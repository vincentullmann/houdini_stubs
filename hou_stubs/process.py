# IMPORT STANDARD LIBRARIES
import os
import re
import sys
from typing import Any, Generator, Optional, Type, Union


# IMPORT THIRD PARTY LIBRARIES
import black
import griffe
from griffe.dataclasses import Alias, Kind, Module, Object, Class, Function, Parameter


# IMPORT LOCAL LIBRARIES
from hou_stubs.parser import docstring
from hou_stubs.parser import cpp


BLACKLIST = [
    "SwigPyIterator",
    "thisown",
    "options",
]


def skip_member(obj: Object) -> bool:

    name = obj.name

    # magic methods
    if name.startswith("__") and name.endswith("__"):
        return True

    if name.startswith("_"):
        return True

    # all the "_FooTuple" Classes
    if re.match(r"_(.+)Tuple", name):
        return True

    if name in BLACKLIST:
        return True

    return False


def process_parameter(parm: Parameter):
    if parm.annotation:
        parm.annotation = str(parm.annotation)
        parm.annotation = docstring.parse(parm.annotation)
        parm.annotation = cpp.parse(parm.annotation)
    # if parm.name == "options":
    #     print(parm)

    pass


def process_function(func: Function):

    # if func.name not in ["averageMinDistance", "globPoints", "orientedPrimBoundingBox"]:
    #     return

    for parameter in func.parameters:
        process_parameter(parameter)

    if False:  # func.docstring:
        text = func.docstring.value or ""
        text = text.split("\n\n")[0]
        text = text.replace("\n", " ")
        match = re.search(r" -> (.+)", text)
        if match:
            func.returns = docstring.parse(match.group(1))
        else:
            func.returns = ""
    else:
        func.returns = cpp.parse(str(func.returns))
        return


def process_class(cls: Class) -> None:
    pass


def process_module(module: Module):
    pass


def process_object(obj: Object):

    obj.members = {k: v for k, v in obj.members.items() if not skip_member(v)}

    # not sure if checking `.obj.KIND` would be besser.
    # but for now.. this plays better with myp
    if isinstance(obj, Module):
        process_module(obj)
    if isinstance(obj, Class):  #  obj.kind == Kind.CLASS:
        process_class(obj)
    if isinstance(obj, Function):
        process_function(obj)

    # members =[m for m in obj.members.values() if not skip(m)]
    for member in obj.members.values():
        if isinstance(member, Object):
            process_object(member)
        else:
            print(member, type(member))

    return obj
