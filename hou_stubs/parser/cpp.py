"""Parse Annotation/Docstrings."""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import re
from dataclasses import dataclass, field

# IMPORT LOCAL LIBRARIES
from hou_stubs.parser import base

################################################################################


CPP_TO_PY = {
    "void": "None",
    "Bool": "bool",
    # str types
    "std::string": "str",
    "String": "str",
    "<class 'str'>": "str",
    "char": "str",
    "BinaryString": "bytes",
    # float and int
    "double": "float",
    "Double": "float",
    "size_t": "int",
    "long": "int",
    "short": "int",
    "int": "int",
    "int64": "int",
    "Int64": "int",
    "std::vector": "list",
    "std::pair": "tuple",
    "std::map": "dict",
    # Objects
    "PyObject": "Any",
    "PY_OpaqueObject": "Any",
    "hboost::any": "Any",
    "swig::SwigPyIterator": "list[Any]",
    "InterpreterObject": "Any",
    "IterableList": "list",
    "HOM_IterableList": "list",
    "HOM_AdvancedDrawable::Params": "dict",
    "HOM_BinaryString": "dict",
    "UT_Tuple": "tuple",
    "EnumTuple": "tuple[EnumValue]",
    # "HOM_logging_MemorySink": "logging.MemorySink",
    # "HOM_logging_LogEntry": "logging.LogEntry",
    # "_logging_LogEntry": "logging.LogEntry",
    # "",
}


@dataclass
class Node:

    name: str
    suffix: str = ""
    children: list["Node"] = field(default_factory=list)
    parent: "Node" | None = None

    def to_python(self) -> str:

        name = self.name

        # "_FooTuple" --> "tuple[Foo]"
        match = re.match(r"^_(.+)Tuple$", name)
        if match:
            name = "tuple"
            inner_type = match.group(1)
            self.children = [Node(name=inner_type)]

        name = CPP_TO_PY.get(name, name)

        # "HOM_logging_LogEntry" --> "hou.logging.LogEntry"
        if name.startswith("HOM_"):
            name = name[4:]
            name = name.replace("_", ".")
            name = f"hou.{name}"

        # remove wrappers
        if name in ("std::allocator", "std::less", "hou.ElemPtr"):
            return self.children[0].to_python()

        if self.suffix in ("size_type",):
            return "int"

        # types with a fixed number of children
        if name in ("list",):
            self.children = [self.children[0]]
        if name in ("dict",):
            self.children = self.children[0:2]

        if self.children:
            children = ", ".join([child.to_python() for child in self.children])
            name = f"{name}[{children}]"

        return name


OPEN = "<"
CLOSE = ">"


def tokenize(string: str) -> Node:
    """Tokenize a string into a Tree of Nodes."""

    # node = Node(name="root")
    # curr: Optional[Node] = None
    # nodes: list[Node] = []
    # depth = 0
    root = Node(name="root")

    # initial values
    node = root
    parent = node

    parts: list[str] = re.findall(rf"{OPEN}|{CLOSE}|[^{OPEN}{CLOSE},]+", string)
    for part in parts:
        part = part.strip()
        # print("1", parent.name, node.name, "PART", part)
        if not part:
            continue

        if part.startswith("::"):
            node.suffix = part[2:]
            continue

        if part == OPEN:
            # starting a new nested block --> all further nodes
            # should be children of the current node
            parent = node
        elif part == CLOSE:
            # closing a block
            node = parent
            parent = node.parent or root
        else:
            node = Node(name=part, parent=parent)
            if parent:
                parent.children.append(node)
    return node


class CppParser(base.Parser):

    fixed_types: dict[str, str] = {}

    replacements: dict[str, str] = {
        "HOM_ViewerDragger::DragValueMap": "dict",
    }

    def pre(self, text) -> str:
        text = super().pre(text)
        # text = re.sub(r"\s*([<>])\s*", r"\1", text)  # remove spaces around "<" and ">"
        text = re.sub(r"\s*,", ",", text)  # remove spaces around commas
        text = text.replace(" *", "")
        text = text.replace(" &", "")
        text = text.replace(" const", "")
        return text

    def main(self, text):
        node = tokenize(text)
        return node.to_python()


parser = CppParser()

parse = parser.parse
