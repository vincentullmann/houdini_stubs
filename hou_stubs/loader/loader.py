# IMPORT THIRD PARTY LIBRARIES
import griffe
from griffe.dataclasses import Module

# IMPORT LOCAL LIBRARIES
from hou_stubs.loader import process


def load_module(name: str, search_paths: list[str] = [], submodules: list[str] = []) -> list[Module]:
    """Load the given module.

    Args:
        name: The name of the module to load.
        search_paths: The paths to search for the module.
    """
    root = griffe.load(module=name, search_paths=search_paths)

    if submodules:
        modules = process.split_submodules(root, *submodules)
    else:
        modules = [root]

    for module in modules:
        module = process.process_object(module)

    return modules
