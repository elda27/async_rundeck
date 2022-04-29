import pytest

import ast
from pathlib import Path

import astor

from dev.impl.convert_api_spec import convert_api_spec

root_dir = Path(__file__).parent / "api"
schemas = [schema_file.stem for schema_file in root_dir.glob("*.yaml")]


@pytest.mark.parametrize(
    "yaml_file, py_file",
    [(f"{prefix}.yaml", f"{prefix}.py") for prefix in schemas],
)
def test_convert_schema(yaml_file: str, py_file: str):
    orig_ast = ast.Module(body=convert_api_spec(root_dir / yaml_file))

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
