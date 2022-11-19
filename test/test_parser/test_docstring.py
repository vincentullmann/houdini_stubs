from hou_stubs.parser import docstring


def test_tuple():
    assert docstring.parse("tuple of Foo") == "tuple[Foo]"


def test_or():
    assert docstring.parse("str or int") == "Union[str, int]"

    # not the cleanest syntax.. but it works
    assert docstring.parse("str or int or float") == "Union[str, int, float]"


def test_dict():
    assert docstring.parse("dict of str to int") == "dict[str, int]"

    assert docstring.parse("dict of [Hom:hou.parmCondType] enum value to string") == "dict[hou.parmCondType, str]"


def test_or_to_union():

    assert docstring.or_to_union("a or b") == "Union[a, b]"
    assert docstring.or_to_union("a or b or c or d") == "Union[a, b, c, d]"
    assert docstring.or_to_union("Union[a, b]") == "Union[a, b]"  # make sure it does't double transform


def test_seq_or_to_union():

    assert docstring.parse("a, b, c or d") == "Union[a, b, c, d]"
    assert docstring.parse("int, float, str, or tuple") == "Union[int, float, str, tuple]"


def test_random_bits():

    # assert docstring.parse("dict of str to any python object`") == "dict[str, Any]"

    # ChannelGraph.selectedKeyframes
    assert docstring.parse("dictionary of (, tuple of hou.BaseKeyframe) pairs") == "dict[str, BaseKeyframe]"

    assert docstring.parse("hou.Color`") == "hou.Color"
    assert docstring.parse("tuple of [Hom:hou.Selection]`") == "tuple[hou.Selection]"
    assert docstring.parse("Qt.QtWidgets.QWidget subclass") == "Qt.QtWidgets.QWidget"

    assert docstring.parse("(tuple of hou.RopNode)") == "tuple[tuple[hou.RopNode]]"


if __name__ == "__main__":
    import sys

    import pytest

    pytest.main(sys.argv)
