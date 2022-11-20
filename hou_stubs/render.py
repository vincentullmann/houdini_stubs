from __future__ import annotations

import os

# IMPORT STANDARD LIBRARIES
from pathlib import Path
from typing import Any

# IMPORT THIRD PARTY LIBRARIES
import black
import jinja2
from griffe.dataclasses import Module

TEMPLATES_PATH = Path(__file__).parent / "templates"

################################################################################


def render_template(template_path: str, **kwargs: Any) -> str:
    """Render Jinja2 template to a string.

    Args:
        template_path (str): Path to the Jinja2 template.
        kwargs: Additional arguments passed to the template

    """
    template_full_path = TEMPLATES_PATH / template_path
    if not template_full_path.exists():
        raise ValueError(f"Template {template_path} not found")

    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATES_PATH),
        trim_blocks=True,
    )

    template = environment.get_template(template_path)
    return template.render(**kwargs)


def blackify(content: str) -> str:
    """Format the given content using black."""
    file_mode = black.FileMode(is_pyi=True, line_length=120)
    try:
        return black.format_file_contents(content, fast=False, mode=file_mode)
    except ValueError as e:  # black.parsing.InvalidInput
        print(">>>>>> INVALID SYNTAX <<<<<<")
        print(e)
        return content


def get_module_filename(module: Module) -> str:

    path = module.canonical_path  # hou.hipFile.foo.bar
    path = path.replace(".", "/")  # hou/hipFile/foo/bar

    if module.modules:
        path = f"{path}/__init__.pyi"  # its a package ("hou/__init__.pyi")
    else:
        path = f"{path}.pyi"  # its a regular module  ("hou/hipFile.pyi")

    # rename the root module. eg.: "hou/hipFile" -> "hou-stubs/hipFile"
    path = path.replace("/", "-stubs/", 1)
    return path


def render_module(module: Module, path: str) -> None:

    # Get the correct template
    template_path = f"static/{module.canonical_path}.pyi.jinja2"
    if not os.path.isfile(TEMPLATES_PATH / template_path):
        template_path = f"base/{module.kind.value}.pyi.jinja2"

    # Render the template
    content = render_template(template_path, module=module)
    content = blackify(content)

    # build the output filepath
    filename = get_module_filename(module)
    filename = os.path.join(path, filename)

    # write
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(content)

    for submodule in module.modules.values():
        render_module(submodule, path)
