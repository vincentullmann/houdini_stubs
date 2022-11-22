import re
import textwrap


def enum_values_from_docstring(docstring: str) -> list[str]:
    r"""Extract Enum Values from a Docstring.
    
    Example:
        >>> enum_values_from_docstring('''\
        >>> Enum values for color channels.
        >>> VALUES
        >>>     red
        >>>         the first channel
        >>>     green
        >>>     blue
        >>>         the color of the sky
        >>> Some Additional Text that shall be omitted
        >>> ''')
        >>> ['red', 'green', 'blue']

    """
    if not re.search(r"\b(Enum values for|Enumeration of) .+\b", docstring):
        return []
    if not "VALUES" in docstring:
        return []

    docstring = textwrap.dedent(docstring)  # align all top level entries
    values_block = docstring.split("VALUES", 1)[-1]

    # extract only indented words
    values = re.findall(r"(?:\s{4})(\w+)\n", values_block)
    return values
