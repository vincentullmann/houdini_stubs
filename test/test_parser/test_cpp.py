from hou_stubs.parser import cpp


def test_parse_fixed_type():

    assert cpp.parse("void") == "None"
    assert cpp.parse("std::string") == "str"
    assert cpp.parse("double") == "float"


################################################################################
# Python Docstrings


################################################################################
# C++ std types


def test_parse():
    """Test std::vector annotation."""
    assert cpp.parse("std::less<Foo>") == "Foo"
    assert cpp.parse("std::allocator<Foo>") == "Foo"
    assert cpp.parse("std::pair<Foo, Bar>") == "tuple[Foo, Bar]"


def test_parse_vector():
    # std::vector
    assert cpp.parse("std::vector<Foo>") == "list[Foo]"
    assert cpp.parse("std::vector < Bar > ") == "list[Bar]"
    assert cpp.parse("std::vector<std::vector<Foo>>") == "list[list[Foo]]"


def test_parse_map():
    assert cpp.parse("std::map<Foo, Bar>") == "dict[Foo, Bar]"
    assert cpp.parse("std::map<Foo , Bar>") == "dict[Foo, Bar]"
    assert cpp.parse("std::map<Foo,Bar,Other,Stuff>") == "dict[Foo, Bar]"


def test_parse_pair():
    assert cpp.parse("std::pair<Foo, Bar>") == "tuple[Foo, Bar]"
    assert cpp.parse("std::pair<list[Foo], Bar>") == "tuple[list[Foo], Bar]"
    assert cpp.parse("std::pair< list[EnumValue],InterpreterObject >") == "tuple[list[EnumValue], Any]"


def test_parse_nested():
    text = "std::vector<std::vector<Foo>>"
    assert cpp.parse(text) == "list[list[Foo]]"


def test_parse_const_pointer():
    assert cpp.parse("Foo *") == "Foo"
    assert cpp.parse("Foo &") == "Foo"
    assert cpp.parse("Foo const &") == "Foo"


def test_parse_examples():
    text = "std::map< std::string,hboost::any,std::less< std::string >,std::allocator< std::pair< std::string const,hboost::any > > > const &"
    assert cpp.parse(text) == "dict[str, Any]"

    text = "std::vector<HOM_ElemPtr<HOM_Vertex>,std::allocator<HOM_ElemPtr<HOM_Vertex>>>"
    assert cpp.parse(text) == "list[hou.Vertex]"

    text = "std::map< HOM_AgentDefinition *,HOM_AgentDefinition * >::size_type"
    assert cpp.parse(text) == "int"


def test_parse_example1():
    #################
    assert cpp.parse("std::vector< HOM_EnumValue *,std::allocator< HOM_EnumValue * >>") == "list[hou.EnumValue]", 1
    assert cpp.parse("std::pair< list[hou.EnumValue],InterpreterObject >") == "tuple[list[hou.EnumValue], Any]", "Step2"

    text = (
        "std::vector<Foo,std::allocator< std::pair< std::vector< HOM_EnumValue *,"
        "std::allocator< HOM_EnumValue * > >,InterpreterObject > > >"
    )
    assert cpp.parse(text) == "list[Foo]", "Step 3"

    text = (
        "std::vector<tuple[list[hou.EnumValue], Any],std::allocator< std::pair< std::vector< HOM_EnumValue *,"
        "std::allocator< HOM_EnumValue * > >,InterpreterObject > > >"
    )
    assert cpp.parse(text) == "list[tuple[list[hou.EnumValue]]", "Step 4"

    # full
    text = (
        "std::vector<std::pair<std::vector< HOM_EnumValue *,"
        "std::allocator<HOM_EnumValue * >>,InterpreterObject >,"
        "std::allocator< std::pair< std::vector< HOM_EnumValue *,std::allocator< HOM_EnumValue * > >,InterpreterObject > > >"
    )
    assert cpp.parse(text) == "list[tuple[list[hou.EnumValue], Any]]", "Step 5"


def test_selectOrientedPositions():
    text = (
        "std::vector< std::pair< HOM_ElemPtr< HOM_Vector3 >,HOM_ElemPtr< HOM_Matrix3 > >,std::allocator"
        "< std::pair< HOM_ElemPtr< HOM_Vector3 >,HOM_ElemPtr< HOM_Matrix3 > > > >"
    )
    assert cpp.parse(text) == "list[tuple[hou.Vector3, hou.Matrix3]]"


def test_example3():
    text = "std::vector< HOM_ParmTuple *,std::allocator< HOM_ParmTuple * > > const &"
    assert cpp.parse(text) == "list[hou.ParmTuple]"


################################################################################

if __name__ == "__main__":
    import sys

    import pytest

    # test_parse()
    pytest.main(sys.argv)
