# IMPORT LOCAL LIBRARIES
from hou_stubs import render
from hou_stubs.loader import loader

################################################################################

SUBMODULES = [
    "hipFile",
    "logging",
    "ui",
]


def main() -> None:

    search_paths = ["/home/vincent-u/dev/hou_stubs/test/data"]
    search_paths = ["/software_local/houdini-19.5/houdini/python3.9libs"]

    module = loader.load_module(
        name="hou",
        search_paths=search_paths,
        submodules=SUBMODULES,
    )

    render.render_module(module, "./typings")


if __name__ == "__main__":
    main()
