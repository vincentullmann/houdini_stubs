# fmt: off

class SomeClass:
    """This is some Class.

    More info about the class.
    """

    some_var: int = 4

    def __init__(self, name: str) -> "void":
        pass

    def some_method(self, foo, bar: int = 4):
        """This is some Method.

        More info about the method.
        """

    def test_less(self,) -> "std::less< foo >":
        ...

    def setData(self, data: "std::map< std::string,hboost::any,std::less< std::string >,std::allocator< std::pair< std::string const,hboost::any > > > const &") -> "void":
        pass

    def evalAsJSONMapsAtFrame(self, frame: "double"):
        r"""

        evalAsJSONMapsAtFrame(self, frame) -> tuple of dict of str to str
        """

    @classmethod
    def decorated(cls, name: str): ...
    def auto_decorated_cls(cls, name: str): ...
    def aut_decorated_static(name: str): ...



def global_method(arg1, arg2: str = "Hey") -> list[int]:
    """This is my Global Method."""
    ...


def implicit_optional(name: str = None): ...


class EmptyClass(type):
    """a class without any members."""

class logging:
    """Class to be exported as its own module."""
    def some_method(self, name: str):
        ...
    def some_method2(self, name: "HOM_logging_sub"): ...


class _logging_sub:
    def stuff(self, name: str): ...


def readInput(self, *args, **kwargs) -> "std::pair< int,std::string >":
    ...
