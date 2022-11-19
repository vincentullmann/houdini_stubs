# IMPORT LOCAL LIBRARIES
from hou_stubs import render
from hou_stubs.loader import loader

################################################################################

# Handritten List of Modules which are defined as classes in the hou.py
# those will be converted into proper modules later
SUBMODULES = [
    "hipFile",
    "logging",
    "ui",
    "hda",
    "ik",
    "crowds",
    "dop",
    "audio",
    "hmath",
    "hotkeys",
    "session",
    "playbar",
    "styles",
    "lop",
    "qt",
    "undos",
    "text",
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
