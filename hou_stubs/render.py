from __future__ import annotations

import os

# IMPORT STANDARD LIBRARIES
from pathlib import Path
from typing import Any

# IMPORT THIRD PARTY LIBRARIES
import black
import jinja2
from griffe.dataclasses import Object

TEMPLATES_PATH = Path(__file__).parent / "templates"


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


def render_obj(obj: Object, path: str, template: str = "module.pyi.jinja2") -> None:

    content = render_template(template, module=obj)
    content = blackify(content)

    # build the output filepath
    filepath = obj.canonical_path.replace(".", "/")
    if obj.modules:
        filepath = f"{filepath}/__init__"
    filepath = f"{path}/{filepath}.pyi"

    # write
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)
