# IMPORT STANDARD LIBRARIES
import os
import re
import sys
from typing import Any, Generator, Optional, Type, Union


# IMPORT THIRD PARTY LIBRARIES
import black
import griffe
from griffe.dataclasses import Alias, Kind, Module, Object, Class, Function, Parameter
from griffe.docstrings.google import parse as parse_google
from griffe.docstrings.parsers import Parser

# IMPORT LOCAL LIBRARIES
from hou_stubs import jinja_env
from hou_stubs import process


################################################################################


def main() -> None:

    search_paths = ["/home/vincent-u/dev/hou_stubs/test"]
    search_paths = ["/software_local/houdini-19.5/houdini/python3.9libs"]
    module = griffe.load(
        module="hou",
        search_paths=search_paths,
        docstring_parser=Parser.google,
    )

    # Process
    process.process_object(module)

    # render template
    content = jinja_env.render_jinja2_template(
        "module.pyi.jinja2",
        module=module,
    )

    # format via black
    file_mode = black.FileMode(is_pyi=False, line_length=120)
    try:
        content = black.format_file_contents(content, fast=True, mode=file_mode)
    except black.InvalidInput as e:
        print(">>>>>> INVALID SYNTAX <<<<<<")
        print(e)

    # write
    with open("./out.pyi", "w") as f:
        f.write(content)


if __name__ == "__main__":
    main()
