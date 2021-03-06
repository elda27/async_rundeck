import pytest

import ast
from pathlib import Path

import astor
import yaml

from dev.impl.convert_schema import _parse_definitions, Property

root_dir = Path(__file__).parent / "schema"
schemas = [schema_file.stem for schema_file in root_dir.glob("*.yaml")]


@pytest.mark.parametrize(
    "yaml_file, py_file",
    [(f"{prefix}.yaml", f"{prefix}.py") for prefix in schemas],
)
def test_convert_schema(yaml_file: str, py_file: str):
    with open(root_dir / yaml_file, "r") as fp:
        definitions = yaml.load(fp, Loader=yaml.SafeLoader)
    definitions = {k: Property(**d) for k, d in definitions.items()}
    orig_ast = ast.Module(body=_parse_definitions(definitions))

    if not (root_dir / py_file).exists():
        with open(root_dir / py_file, "w+") as fp:
            fp.write(astor.to_source(orig_ast))
    else:
        out_file = root_dir / py_file
        with open(out_file, "r") as fp:
            ans_ast = fp.read()
        with open(out_file.with_name(out_file.stem + ".test.py"), "w+") as fp:
            fp.write(astor.to_source(orig_ast))

        assert astor.to_source(orig_ast) == ans_ast
