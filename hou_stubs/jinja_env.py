from __future__ import annotations

from pathlib import Path
from typing import Any

import jinja2
from griffe.dataclasses import Expression, Name

TEMPLATES_PATH = Path(__file__).parent / "templates"

HOU_TO_PY_TYPE = {
    "void": None,
    "size_t": int,
    "std::string": str,
    "char const *": str,
    "_FloatTuple": tuple[float],
    "double": float,
}


def format_annotation(annotation: str | Name | Expression | None) -> str | None:
    print("format_annotation", annotation)
    if not annotation:
        return ""
    annotation = str(annotation)
    return HOU_TO_PY_TYPE.get(annotation, annotation)
    # annotation = str(annotation)
    # if isinstance(annotation, str):
    return annotation
    # if annotation in HOU_TO_PY_TYPE:
    return
    # return str(annotation)
    # return HOU_TO_PY_TYPE.get(annotation, annotation)


# {%- if parameter.annotation -%}
# {%- with expression = parameter.annotation -%}
# {{ " : " }}{{ expression.source -}}
# {%- endwith -%}
# {%- endif -%}

formatters = {
    "format_annotation": format_annotation,
}


def render_jinja2_template(template_path: str, **kwargs: Any) -> str:
    """
    Render Jinja2 template to a string.

    Arguments:
        template_path -- Relative path to template in `TEMPLATES_PATH`
        module -- Module record.
        service_name -- ServiceName instance.

    Returns:
        A rendered template.
    """
    template_full_path = TEMPLATES_PATH / template_path
    if not template_full_path.exists():
        raise ValueError(f"Template {template_path} not found")

    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATES_PATH),
    )

    template = environment.get_template(template_path)
    template.globals.update(formatters)
    return template.render(**kwargs)  # , service_name=service_name)
