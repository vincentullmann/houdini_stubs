import re
from hou_stubs.parser import base


def or_to_union(text: str):
    """Format a match of multiple items into a "Union"-Annotation.

    Example:
        >>> or_to_union("foo or bar or baz")
        Union[foo, bar, baz]
        >>> or_to_union("a, b, c or d")
        Union[a, b, c, d]
    """

    # only process if it matches the pattern
    if not " or " in text:
        return text

    text = text.replace("or", ",").replace(" ", "")
    parts = text.split(",")
    parts = [p for p in parts if p]
    if len(parts) == 1:
        return parts[0]

    parts = ", ".join(parts)
    return f"Union[{parts}]"


def multi_or_to_union(match: re.Match):
    """Format a match of multiple items into a "Union"-Annotation.

    Example:
        >>> multi_or_to_union("a, b, c or d")
        Union[a, b, c, d]
    """
    text = match.group(0)
    print("multi_or_to_union 1", text)
    text = text.replace(", or ", " or ")  # for cases like "a, b, or c"  (note the comma after b)
    print("multi_or_to_union 2", text)
    text = text.replace(", ", " or ")
    return ""
    return or_to_union(text)


class DocstringParser(base.Parser):

    replacements: dict[str, str] = {
        "any python object`": "Any",
        "any python obect": "Any",
        "any python object": "Any",
        "str for Python 2, bytes for Python 3": "bytes",
        "generator": "Generator",
        "dictionary of (, tuple of hou.BaseKeyframe) pairs": "dict[str, BaseKeyframe]",  # hou.ChannelGraph.selectedKeyframes
        "(start, end)": "tuple[int, int]",  # ChopNode.sampleRange
        "(float, float, float)": "tuple[float, float, float]",  # hou.Color
        "HOM_AdvancedDrawable::Params const &": "Any",
        "dict of [Hom:hou.parmCondType] enum value to string": "dict[hou.parmCondType, str]",
        "`": "",  # remove some random backticks scattered around
        "tuples": "tuple",
        "(hou.ObjNode, str)": "tuple[hou.ObjNode, str]",  # hipFile.importFBX
    }

    patterns: base.PATTERNS_TYPE = [
        (r"^\((.+)\)$", r"tuple[\1]"),  # --> "(Foo, Bar)" -> "tuple[Foo, Bar]"
        (r"dict of (.+) to (.+)", r"dict[\1, \2]"),  # "dict of str to int" --> "dict[str, int]"
        (r"(.+?) of (.+)", r"\1[\2]"),  # "tuple of hou.Point" --> "tuple[hou.Point]"
        (r"(.+) enum value", r"\1"),  # "Foo enum value" -> "Foo",
        # (r"(?:(\w+),\s*)+or (\w+)", multi_or_to_union),
        # (r"(?:(\w+),\s*)+or (\w+)", or_to_union),
        # (r"\`$", ""),
        (r"\[Hom\:(hou\.\w+)\]", r"\1"),  # [Hom:hou.Selection] -> hou.Selection
        (r"(.+) subclass", r"\1"),
    ]

    formatters = [
        or_to_union,
    ]

    def pre(self, text: str) -> str:
        return super().pre(text)


parser = DocstringParser()

parse = parser.parse
