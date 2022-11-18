from hou_stubs.parser import base


def test_node_simple():
    node = base.Node.from_str("foo")
    assert node.name == "foo"
    assert node.children == []


def test_node_from_string_1():

    node = base.Node.from_str("foo[A, B, C]")
    assert node.name == "foo"


if __name__ == "__main__":
    import pytest
    import sys

    pytest.main(sys.argv)
