from pathlib import Path
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple
import ast

import stringcase
import yaml
from pydantic import BaseModel
import astor

from dev.impl.convert_schema import (
    _parse_definition,
    Property,
    _as_optional_if_required,
)
from dev.impl.special_cases import special_case_property

ParameterTypes = Literal["query", "path", "header", "cookie", "body"]


class ApiSpec(BaseModel):
    pass


def convert_api_specs(api_spec_dir: Path) -> Dict[str, ast.AST]:
    asts = {}
    for spec_file in (api_spec_dir / "rundeck").glob("*.yaml"):
        if spec_file.name == "definitions.yaml":
            continue
        asts[spec_file.stem] = convert_api_spec(spec_file)
    return asts


def convert_api_spec(spec_file: Path) -> ast.AST:
    with open(spec_file) as fp:
        spec = yaml.load(fp)

    functions = []
    cache: Dict[str, ast.ClassDef] = {}
    for url, details in spec["paths"].items():
        version = int(url.split("/")[2])

        for method, detail in details.items():
            responses = _get_returns(detail, cache)
            response_ast = None
            if len(responses) > 1:
                response_ast = ast.Subscript(
                    value=ast.Name(id="Union", ctx=ast.Load()),
                    slice=ast.Index(
                        value=ast.Tuple(elts=list(responses.values()), ctx=ast.Load())
                    ),
                    ctx=ast.Load(),
                )
            else:
                response_ast = list(responses.values())[0]

            parameters, kw_parameters, defaults = _get_parameters(detail, cache)
            arg_defaults = []
            for pos in parameters.keys():
                arg_defaults.extend(
                    [defaults[k] for k in parameters[pos].keys() if k in defaults]
                )
            kw_defaults = []
            for pos in kw_parameters.keys():
                kw_defaults.extend(
                    [
                        defaults.get(k, ast.Constant(value=None))
                        for k in kw_parameters[pos].keys()
                    ]
                )

            functions.append(
                ast.AsyncFunctionDef(
                    name=stringcase.snakecase(detail.get("operationId")),
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[
                            ast.arg(
                                arg="session",
                                annotation=ast.Name(id="RundeckClient", ctx=ast.Load()),
                                type_comment=None,
                            ),
                            ast.arg(
                                arg="entrypoint",
                                annotation=ast.Name(id="str", ctx=ast.Load()),
                                type_comment=None,
                            ),
                            ast.arg(
                                arg="version",
                                annotation=ast.Name(id="int", ctx=ast.Load()),
                                type_comment=None,
                            ),
                        ]
                        + sum(
                            [list(params.values()) for params in parameters.values()],
                            start=[],
                        ),
                        defaults=arg_defaults,
                        vararg=None,
                        kwonlyargs=sum(
                            [
                                list(params.values())
                                for params in kw_parameters.values()
                            ],
                            start=[],
                        ),
                        kw_defaults=kw_defaults,
                        kwarg=None,
                    ),
                    body=[
                        ast.Expr(
                            ast.Constant(
                                value="\n".join([detail.get("summary", "")]), kind=None
                            )
                        ),
                    ]
                    + generate_body(
                        method=method,
                        version=version,
                        path=url,
                        parameters=dict(**parameters, **kw_parameters),
                        responses=responses,
                    ),
                    decorator_list=[],
                    returns=response_ast,
                    type_comment=None,
                )
            )

    defined_classes = []
    new_classes = []
    for name, classdef in cache.items():
        if classdef is None:
            defined_classes.append(ast.alias(name=name, asname=None))
        else:
            new_classes.append(classdef)

    import_statements = [
        ast.ImportFrom(
            module="async_rundeck.client",
            names=[ast.alias(name="RundeckClient", asname=None)],
            level=0,
        ),
        ast.ImportFrom(
            module="async_rundeck.exceptions",
            names=[
                ast.alias(name="RundeckError", asname=None),
                ast.alias(name="VersionError", asname=None),
            ],
            level=0,
        ),
    ]
    if len(defined_classes) > 0:
        defined_classes.append(
            ast.ImportFrom(
                module="async_rundeck.proto.definitions", names=defined_classes, level=0
            )
        )
    return import_statements + new_classes + functions


def _get_returns(
    detail: Dict[str, Any], cache: Dict[str, ast.ClassDef] = {}
) -> Dict[str, Optional[ast.AST]]:
    responses = {}
    for code, response in detail["responses"].items():
        if "schema" in response:
            schema = response["schema"]

            if "type" in schema or "$ref" in schema:
                schema = response["schema"]
                type_id = stringcase.pascalcase(detail["operationId"]) + "Response"
                ann_assign = _parse_definition(
                    type_id,
                    Property.parse_obj(schema),
                    cache,
                )
                responses[code] = ann_assign.annotation
            else:
                type_id = stringcase.pascalcase(detail["operationId"]) + "Response"
                _parse_definition(
                    type_id,
                    Property.parse_obj(schema),
                    cache,
                )
                responses[code] = ast.Name(id=type_id, ctx=ast.Load())
        else:
            responses[code] = ast.Constant(value=None)
    return responses


def _get_parameters(
    detail: Dict[str, Any], cache: Dict[str, ast.ClassDef] = {}
) -> Tuple[
    Dict[ParameterTypes, Dict[str, ast.AST]],
    Dict[ParameterTypes, Dict[str, ast.AST]],
    Dict[str, ast.AST],
]:
    parameters = {}
    kw_parameters = {}
    defaults = {}
    flatten_str = {}
    for param in detail.get("parameters", []):
        param_name = param["name"]
        if param_name in special_case_property:
            param_name = special_case_property[param_name]
        else:
            param_name = stringcase.snakecase(param_name)

        if "schema" in param:
            ann_assign = _parse_definition(
                param_name, Property.parse_obj(param["schema"]), cache
            )
            type_id = astor.to_source(ann_assign.annotation)
            if type_id.startswith("Optional"):
                type_id = type_id[8:].strip("[]\n")
            if type_id not in cache:
                cache[type_id] = None
        else:
            type_id = stringcase.pascalcase(param["type"])
        required = param.get("required", False)
        type = _as_optional_if_required(
            ast.Name(id=type_id, ctx=ast.Load()),
            required=required,
        )
        if required:
            parameters.setdefault(param["in"], {})[param_name] = ast.arg(
                arg=param_name,
                annotation=type,
                type_comment=None,
            )
        else:
            kw_parameters.setdefault(param["in"], {})[param_name] = ast.arg(
                arg=param_name,
                annotation=type,
                type_comment=None,
            )
        if "default" in param:
            defaults[param_name] = ast.Constant(value=param["default"], kind=None)
    return parameters, kw_parameters, defaults


function_body = """async def func(client: "RundeckClient", **kwargs) -> T:
    if version < {version}:
        raise VersionError(f"Insufficient api version error, Required >{version}")
    url = entrypoint + "{path}".format(version=version, {path_kws})
    async with session.request("{method}", url, data={body_kws}, params={query_kws}) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {responses}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {{url}}({{response.status}})")
        else:
            raise RundeckError(
                f"Connection diffused: {{url}}({{response.status}})\\n{{obj}}")
"""


def generate_body(
    method: str,
    version: int,
    path: str,
    parameters: Dict[ParameterTypes, Dict[str, ast.AST]],
    responses: Dict[int, ast.Name],
) -> ast.AST:
    return (
        ast.parse(
            function_body.format(
                version=version,
                method=method.upper(),
                path=path.replace(f"/api/{version}", "/api/{version}"),
                path_kws=", ".join(
                    [f"{k}={k}" for k in parameters.get("path", {}).keys()]
                ),
                query_kws="dict({})".format(
                    ",".join([f"{k}={k}" for k in parameters.get("query", {}).keys()])
                ),
                body_kws="dict({})".format(
                    ",".join(
                        [f"**{k}.dict()" for k in parameters.get("body", {}).keys()]
                    )
                ),
                responses="{"
                + (
                    ",".join(
                        [f"'{k}':{astor.to_source(t)}" for k, t in responses.items()]
                    )
                )
                + "}",
            )
        )
        .body[0]
        .body
    )
