#!/usr/bin/env python
"""Generate Stub Files for Houdini's Python Module.

Usage:
    >>> hou_stubs/main.py test/data/hou.py
    >>> hou_stubs/main.py /software_local/houdini-19.5/houdini/python3.9libs/hou.py
"""

# IMPORT STANDARD LIBRARIES
import argparse
import os
import shutil

# IMPORT LOCAL LIBRARIES
from hou_stubs import render
from hou_stubs.loader import loader

################################################################################

# Handritten List of Modules which are defined as classes in the hou.py
# those will be converted into proper modules later
SUBMODULES = [
    "anonstats",
    "audio",
    "clone",
    "crowds",
    "dop",
    "galleries",
    "hda",
    "hipFile",
    "hmath",
    "hotkeys",
    "ik",
    "logging",
    "lop",
    "perfMon",
    "playbar",
    "properties",
    "pypanel",
    "qt",
    "session",
    "shelves",
    "styles",
    "takes",
    "text",
    "ui",
    "undos",
    "viewportVisualizers",
]


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        prog="Houdini Stub Generator",
        description="generates houdini stub files.",
    )
    parser.add_argument("path")
    parser.add_argument("-o", "--out", help="Output directory", default="./typings")
    parser.add_argument("--clean", help="clean the output directory", action="store_true")
    return parser.parse_args()


def main() -> None:

    args = parse_args()

    path = args.path
    search_paths = [os.path.dirname(path)]
    module_name, _ = os.path.splitext(os.path.basename(path))

    module = loader.load_module(
        name=module_name,
        search_paths=search_paths,
        submodules=SUBMODULES,
    )

    if args.clean:
        print(f"deleting {args.out}!")
        shutil.rmtree(args.out)

    render.render_module(module, args.out)


if __name__ == "__main__":
    main()
