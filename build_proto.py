import ast
from functools import partial
import subprocess
from argparse import ArgumentParser
from tempfile import TemporaryDirectory
from pathlib import Path
import subprocess

import astor


from dev.impl.convert_schema import convert_schema
from dev.impl.convert_api_spec import convert_api_specs

special_case_class = {"os": "OS"}


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-w",
        "--work-dir",
        type=Path,
        default=None,
        help="Working directory, if None a temporary directory will be created.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("./async_rundeck/proto/"),
        help="Output directory",
    )
    args = parser.parse_args()

    output_dir = args.output_dir or Path()
    if args.work_dir is None:
        with TemporaryDirectory() as work_dir:
            create_scripts(Path(work_dir), output_dir)
    else:
        work_dir.mkdir(exist_ok=True)
        create_scripts(Path(work_dir), output_dir)


def create_scripts(work_dir: Path, output_dir: Path) -> None:
    api_spec_dir = work_dir / "rundeck-api-specs"
    clone_repo(api_spec_dir)

    module_ast = convert_schema(api_spec_dir)

    with open(output_dir / "definitions.py", "w+") as fp:
        fp.write("# DON'T CHANGE MANUALLY THIS FILE.\n")
        fp.write(
            "# This file is generated from https://github.com/rundeck/rundeck-api-specs\n"
        )
        fp.write(astor.to_source(module_ast))

    asts = convert_api_specs(api_spec_dir)
    for key, body_ast in asts.items():
        with open(output_dir / f"{key}.py", "w+") as fp:
            fp.write("# DON'T CHANGE MANUALLY THIS FILE.\n")
            fp.write(
                "# This file is generated from https://github.com/rundeck/rundeck-api-specs\n"
            )
            fp.write(
                astor.to_source(
                    ast.Module(
                        body=[
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
                                ],
                                level=0,
                            ),
                            ast.ImportFrom(
                                module="pydantic",
                                names=[
                                    ast.alias(name="BaseModel", asname=None),
                                    ast.alias(name="Field", asname=None),
                                    ast.alias(name="parse_obj_as", asname=None),
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
                                    ast.alias(name="File", asname=None),
                                ],
                                level=0,
                            ),
                        ]
                        + body_ast,
                        type_ignores=[],
                    ),
                    source_generator_class=PatchedSourceGenerator,
                )
            )

    try:
        subprocess.call(["black", str(Path(__file__).parent / "async_rundeck/proto/")])
    except SystemExit:
        pass


def clone_repo(api_spec_dir: Path):
    if not api_spec_dir.exists():
        subprocess.check_call(
            f"git clone -b patch https://github.com/elda27/rundeck-api-specs {api_spec_dir}",
            # Temporaly commented out to avoid some issues
            # f"git clone https://github.com/rundeck/rundeck-api-specs {api_spec_dir}",
            shell=True,
        )


from astor.op_util import Precedence
from astor.code_gen import set_precedence


class PatchedSourceGenerator(astor.SourceGenerator):
    def visit_ImportFrom(self, node):
        self.statement(node, "from ", node.level * ".", node.module or "", " import ")
        self.comma_list_with_bracket(node.names)
        # Goofy stuff for Python 2.7 _pyio module
        if node.module == "__future__" and "unicode_literals" in (
            x.name for x in node.names
        ):
            self.using_unicode_literals = True

    def comma_list_with_bracket(self, items, trailing=False):
        set_precedence(Precedence.Comma, *items)
        self.write("(")
        for idx, item in enumerate(items):
            self.write(", " if idx else "", item)
        self.write("," if trailing else "")
        self.write(")")


if __name__ == "__main__":
    main()
