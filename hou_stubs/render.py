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


def file_exists(path) -> bool:
    """Test whether a file exists or not."""
    return os.path.exists(TEMPLATES_PATH / path)


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

    kwargs.update(
        {
            "file_exists": file_exists,  # required for conditional "include" of static files
        }
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


def render_module(module: Module, path: str) -> None:

    # build the output filepath
    filename = module.canonical_path.replace(".", "/")
    filename = os.path.join(path, filename)

    if module.modules:
        filename = f"{filename}/__init__.pyi"  # its a package
        for submodule in module.modules.values():
            render_module(submodule, path)
    else:
        filename = f"{filename}.pyi"  # its a regular module

    # Render the template
    content = render_template("module.pyi.jinja2", module=module)
    content = blackify(content)

    # write
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(content)
