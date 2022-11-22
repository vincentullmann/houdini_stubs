import sys

import pytest

from hou_stubs.loader import process_utils


class Test_enum_values_from_docstring:
    def test_ignores_wrong_type(self):
        """Do return empty list for invalid docstrings."""
        docstring = "Foo Bar"
        assert process_utils.enum_values_from_docstring(docstring) == []

    def test_extract_values(self):
        docstring = """
        Enum values for color channels.

        VALUES
            red
            green
            blue

        """
        assert process_utils.enum_values_from_docstring(docstring) == ["red", "green", "blue"]

    def test_extract_values_trailing_info(self):
        docstring = """
        Enum values for color channels.

        VALUES
            red
            green
            blue
        
        Some Additional Text that shall be omitted
        """
        assert process_utils.enum_values_from_docstring(docstring) == ["red", "green", "blue"]

    def test_extract_values_multiline_value(self):
        docstring = """
        Enum values for color channels.

        VALUES
            red
                the first channel
            green
            blue
                the color of the sky
        
        Some Additional Text that shall be omitted
        """
        assert process_utils.enum_values_from_docstring(docstring) == ["red", "green", "blue"]


################################################################################

if __name__ == "__main__":
    pytest.main(sys.argv)
