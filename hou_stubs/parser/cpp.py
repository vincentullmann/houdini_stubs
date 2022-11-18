"""Parse Annotation/Docstrings."""

from dataclasses import dataclass, field
import re
from typing import ClassVar, Optional

from hou_stubs.parser import base


################################################################################


CPP_TO_PY = {
    "void": "None",
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
    "int64": "int",
    "Int64": "int",
    "std::vector": "list",
    "std::pair": "tuple",
    "std::map": "dict",
    # Objects
    "PyObject": "Any",
    "hboost::any": "Any",
    "swig::SwigPyIterator": "list[Any]",
    "InterpreterObject": "Any",
    "HOM_AdvancedDrawable::Params": "dict",
    # "",
}


@dataclass
class Node:

    name: str
    suffix: str = ""
    children: list["Node"] = field(default_factory=list)
    parent: "Node" = None

    def to_python(self) -> str:

        name = CPP_TO_PY.get(self.name) or self.name

        # remove wrappers
        if name in ("std::allocator", "std::less", "ElemPtr"):
            return self.children[0].to_python()

        if self.suffix in ("size_type",):
            return "int"

        # types with a fixed number of children
        if name in ("list",):
            self.children = [self.children[0]]
        if name in ("dict",):
            self.children = self.children[0:2]

        if self.children:
            children = [child.to_python() for child in self.children]
            children = ", ".join(children)
            # children = f"({children})"
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
    node = Node(name="root")
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
            parent = node.parent
        else:
            node = Node(name=part, parent=parent)
            if parent:
                parent.children.append(node)
    return node


def remove_pointer(text):
    """Remove pointer from text."""
    return re.sub(r"^\s*Pointer\s+<([^<>]+)>", r"\1", text)


class CppParser(base.Parser):

    fixed_types: dict[str, str] = {}

    replacements: dict[str, str] = {
        "HOM_ViewerDragger::DragValueMap": "dict",
    }

    patterns: base.PATTERNS_TYPE = [
        # (r"\s*<\s*", "<"),
        # (r"\s*>\s*", ">"),
        # Pointer/Const
        (r"(.+\S)\s*(\*|\&|const)+", r"\1"),
        # C++ std
        (r"std::\w+<([^<>]+)>::size_type", r"int"),
        (r"std::\w+<([^<>]+)>::iterator", r"int"),
        (r"std::less<([^<>]+)>", r"\1"),  # "std::less<Foo>" == "Foo"
        (r"std::allocator<([^<>]+)>", r"\1"),  # "std::allocator<Foo>" == "Foo"
        # # (r"std::vector<([^<>]+)>", r"list[\1]"),  # "std::vector<Foo>" == "list[Foo]"
        (r"std::vector<([^<>,]+)(,[^<>]+)*>", r"list[\1]"),  # "std::vector<Foo,X,Y,Z>" == "list[Foo]"
        (r"std::pair<([^<>]+)\s*,\s*([^>]+)>", r"tuple[\1, \2]"),  # "std::pair<Foo, Bar>" == "tuple[Foo, Bar]"
        (r"std::map<([^<>]+?)\s*,\s*([^<>,]+)[^>]*>", r"dict[\1, \2]"),  # "std::map<Foo, Bar>" == "dict[Foo, Bar]"
        # # HOM
        (r"HOM_ElemPtr<([^<>]+)>", r"\1"),  # "HOM_ElemPtr<Foo>" -> "Foo"
        (r"HOM_IterableList<([^<>]+)>", r"list[\1]"),  # "HOM_IterableList<Foo>" -> "list[Foo"
        (r"HOM_([^<>]+)", r"\1"),
    ]

    def pre(self, text) -> str:
        text = super().pre(text)
        # text = re.sub(r"\s*([<>])\s*", r"\1", text)  # remove spaces around "<" and ">"
        text = re.sub(r"\s*,", ",", text)  # remove spaces around commas
        text = text.replace(" *", "")
        text = text.replace(" &", "")
        text = text.replace(" const", "")
        text = text.replace("HOM_", "")  # "HOM_Vertex" -> "Vertex"
        return text

    def main(self, text):
        node = tokenize(text)
        return node.to_python()


parser = CppParser()

parse = parser.parse


# node = parse_string("foo<bar, b<b1, <b2>>>")
# print("##################")
# print("R:", node)
# # node.print_tree()
# print(format_node(node))
