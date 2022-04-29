from pathlib import Path
from typing import Any, Dict, List, Optional, OrderedDict
import stringcase

import yaml
import ast
from pydantic import BaseModel, Field
from dev.impl.special_cases import special_case_property


class Property(BaseModel):
    type: Optional[str]
    required: Optional[List[str]]
    properties: Optional[Dict[str, "Property"]]
    items: Optional["Property"]
    enum: Optional[List[Any]]
    ref: str = Field(None, alias="$ref")
    description: Optional[str]


Property.update_forward_refs()


def convert_schema(api_spec_dir: Path) -> ast.Module:
    with open(api_spec_dir / "rundeck" / "definitions.yaml", "r") as fp:
        definitions = yaml.load(fp, Loader=yaml.SafeLoader)
    definitions = {k: Property(**d) for k, d in definitions.items()}
    definitions = _parse_definitions(definitions)
    return ast.Module(
        [
            ast.ImportFrom(
                module="enum",
                names=[
                    ast.alias(name="Enum", asname=None),
                ],
                level=0,
            ),
            ast.ImportFrom(
                module="typing",
                names=[
                    ast.alias(name="List", asname=None),
                    ast.alias(name="Optional", asname=None),
                    ast.alias(name="Union", asname=None),
                ],
                level=0,
            ),
            ast.ImportFrom(
                module="pydantic",
                names=[
                    ast.alias(name="BaseModel", asname=None),
                    ast.alias(name="Field", asname=None),
                ],
                level=0,
            ),
            ast.ImportFrom(
                module="async_rundeck.proto.json_types",
                names=[
                    ast.alias(name="Integer", asname=None),
                    ast.alias(name="Number", asname=None),
                    ast.alias(name="String", asname=None),
                    ast.alias(name="Boolean", asname=None),
                    ast.alias(name="Object", asname=None),
                ],
                level=0,
            ),
        ]
        + definitions
    )


def _parse_definitions(definitions: Dict[str, Property]) -> List[ast.AST]:
    """Parse definitions into a dictionary of ASTs and a dictionary of definitions

    Parameters
    ----------
    definitions : Dict[str, Property]
        JSON Schema definitions

    Returns
    -------
    Tuple[Dict[str, str], List[str]]
        _description_
    """
    definitions_cache = OrderedDict()
    for name, definition in definitions.items():
        definitions_cache[name] = _parse_definition(
            name, definition, definitions_cache, top_level=True
        )

    return list(filter(lambda x: x is not None, definitions_cache.values()))


def _parse_definition(
    name: str,
    definition: Property,
    definitions_cache: Dict[str, ast.ClassDef],
    *,
    top_level=False,
    refs: Dict[str, str] = None,
    **kwargs,
) -> ast.AST:
    """Parse definition from JSON schema

    Parameters
    ----------
    name : str
        Name of the parent field
    definition : Property
        definition to parse
    definitions_cache : Dict[str, ast.ClassDef]
        cache of classes if definition field has nested schema
    top_level : bool, optional
        To detect recursion call, by default False
    refs : Dict[str, str], optional
        Storing found references, by default None

    Returns
    -------
    ast.AST
        Parsed abstract syntax tree
    """
    if definition.enum is not None:
        return _parse_enum(
            name,
            definition,
            definitions_cache,
            top_level=top_level,
            # refs=refs,
            **kwargs,
        )
    elif definition.type is not None:
        if definition.type == "array":
            return _parse_array(
                name, definition, definitions_cache, refs=refs, **kwargs
            )
        else:
            return _parse_value(
                name, definition, definitions_cache, refs=refs, **kwargs
            )
    elif definition.ref is not None:
        return _parse_value(name, definition, definitions_cache, refs=refs, **kwargs)
    else:  # Class declaration
        if top_level:
            klass = _parse_class_def(
                name, definition, definitions_cache, refs=refs, **kwargs
            )
            definitions_cache[klass.name] = None
            return klass
        else:
            # Special case for nested classes
            klass = _parse_class_def(
                name, definition, definitions_cache, refs=refs, **kwargs
            )
            definitions_cache[klass.name] = klass
            return ast.AnnAssign(
                target=ast.Name(id=stringcase.snakecase(name), ctx=ast.Store()),
                annotation=_as_optional_if_required(
                    ast.Name(id=klass.name, ctx=ast.Load()),
                    kwargs.get("required", False),
                ),
                # value=None,
                value=ast.Call(
                    func=ast.Name(id="Field", ctx=ast.Load()),
                    args=[],
                    keywords=[
                        ast.keyword(
                            arg="alias", value=ast.Constant(value=name, kind=None)
                        )
                    ],
                ),
                simple=1,
            )


def _parse_class_def(
    name: str,
    definition: Property,
    definitions_cache: Dict[str, ast.ClassDef],
    required: bool = False,
    **kwargs,
) -> ast.AST:
    required = definition.required or []

    return ast.ClassDef(
        name=stringcase.pascalcase(name),
        bases=[ast.Name(id="BaseModel", ctx=ast.Load())],  # derrived pydantic.BaseModel
        decorator_list=[],
        body=[
            _parse_definition(
                child_name,
                child_prop,
                definitions_cache,
                required=child_name in required,
                **kwargs,
            )
            for child_name, child_prop in definition.properties.items()
        ],
    )


def _as_optional_if_required(type_ast: ast.AST, required: bool) -> ast.Subscript:
    if required:
        return type_ast
    else:
        return ast.Subscript(
            value=ast.Name(id="Optional", ctx=ast.Load()),
            slice=ast.Index(value=type_ast),
        )


def _format_type(type: str, cache: Dict[str, str]) -> str:
    type_id = stringcase.pascalcase(type)
    if type_id not in cache and type_id not in [
        "Integer",
        "Number",
        "String",
        "Boolean",
        "Object",
    ]:
        type_id = f'"{type_id}"'
    return type_id


def _format_property_name(name: str) -> str:
    if name in special_case_property:
        return special_case_property[name]
    else:
        return stringcase.snakecase(name)


def _parse_value(
    name: str,
    definition: Property,
    cache: Dict[str, str],
    *,
    required=True,
    refs: Dict[str, str] = None,
) -> ast.AnnAssign:
    if definition.ref is not None:
        type = definition.ref.split("/")[-1]
        if refs is not None and type not in refs:
            refs[definition.ref] = type
    else:
        type = definition.type

    return ast.AnnAssign(
        target=ast.Name(id=_format_property_name(name), ctx=ast.Store()),
        annotation=_as_optional_if_required(
            ast.Name(id=_format_type(type, cache), ctx=ast.Load()), required
        ),
        value=ast.Call(
            func=ast.Name(id="Field", ctx=ast.Load()),
            args=[],
            keywords=[
                ast.keyword(arg="alias", value=ast.Constant(value=name, kind=None))
            ],
        ),
        simple=1,
    )


def _parse_array(
    name: str,
    definition: Property,
    cache: Dict[str, str],
    *,
    required=True,
    refs: Dict[str, str] = None,
) -> ast.AnnAssign:
    if definition.items is not None:
        if definition.items.ref is not None:
            type = definition.items.ref.split("/")[-1]
            if refs is not None and type not in refs:
                refs[definition.items.ref] = type
        else:
            type = definition.items.type
    else:
        type = definition.type

    return ast.AnnAssign(
        target=ast.Name(id=_format_property_name(name), ctx=ast.Store()),
        annotation=_as_optional_if_required(
            ast.Subscript(
                value=ast.Name(id="List", ctx=ast.Load()),
                slice=ast.Index(
                    value=ast.Name(id=_format_type(type, cache), ctx=ast.Load())
                ),
            ),
            required=required,
        ),
        value=ast.Call(
            func=ast.Name(id="Field", ctx=ast.Load()),
            args=[],
            keywords=[
                ast.keyword(arg="alias", value=ast.Constant(value=name, kind=None))
            ],
        ),
        simple=1,
    )


def _parse_enum(
    name: str,
    definition: Property,
    cache: Dict[str, str],
    top_level=False,
    required=False,
) -> ast.ClassDef:
    type_id = stringcase.pascalcase(name)
    enum = ast.ClassDef(
        name=type_id,
        bases=[ast.Name(id="Enum", ctx=ast.Load())],
        keywords=[],
        decorator_list=[],
        body=[
            ast.Assign(
                [ast.Name(id=stringcase.pascalcase(value.title()), ctx=ast.Store())],
                value=ast.Constant(value=value, kind=None),
            )
            for value in definition.enum
        ],
    )
    if top_level:
        cache[type_id] = None
        return enum
    else:
        cache[type_id] = enum
        return ast.AnnAssign(
            target=ast.Name(id=_format_property_name(name), ctx=ast.Store()),
            annotation=_as_optional_if_required(
                ast.Name(id=_format_type(type_id, cache), ctx=ast.Load()), required
            ),
            value=ast.Call(
                func=ast.Name(id="Field", ctx=ast.Load()),
                args=[],
                keywords=[
                    ast.keyword(arg="alias", value=ast.Constant(value=name, kind=None))
                ],
            ),
            simple=1,
        )
