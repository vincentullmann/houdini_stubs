import os
import sys

import black
import griffe

from hou_stubs import jinja_env


def main() -> None:

    search_paths = ["/home/vincent-u/dev/hou_stubs/test"]
    search_paths = ["/software/houdini-19.5/houdini/python3.9libs"]
    module = griffe.load(module="hou", search_paths=search_paths)

    # render template
    content = jinja_env.render_jinja2_template(
        "module.pyi.jinja2",
        module=module,
    )

    # format via black
    # file_mode = black.FileMode(is_pyi=False)  # , line_length=120)
    # content = black.format_file_contents(content, fast=True, mode=file_mode)
    # print(content)

    # write
    with open("./out.py", "w") as f:
        f.write(content)


if __name__ == "__main__":
    main()
