from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import re

# IMPORT THIRD PARTY LIBRARIES
from griffe.dataclasses import Alias, Attribute, Class, Decorator, Function, Module, Object, Parameter
from griffe.expressions import Expression, Name

# IMPORT LOCAL LIBRARIES
from hou_stubs.loader import process_utils
from hou_stubs.parser import cpp, docstring

BLACKLIST = [
    "SwigPyIterator",
    "thisown",
    "options",
    "_orig_hou",
    "cvar",
    "_guDetailHandle",
    "_geometryHandle",
]


def remove_prefix(text: str, prefix: str):
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def skip_member(obj: Object | Alias) -> bool:

    name = obj.name

    # magic methods
    if name.startswith("__") and name.endswith("__"):
        return True

    # all the "_FooTuple" Classes
    if re.match(r"_(.+)Tuple", name):
        return True

    if name in BLACKLIST:
        return True

    return False


################################################################################
# Logic to split "fake modules" into proper sub-modules
#


def _extract_module(root: Module, name: str) -> Module | None:
    # modules.append(module)
    # module.kind = Kind.MODULE
    try:
        source = root.members.pop(name)
    except KeyError:
        return None

    module = Module(name=name, parent=root)
    module.members = source.members
    root.members[name] = module

    # update the parent ref
    for member in module.members.values():
        member.parent = module

    # remove the "self" paramater from all methods
    # as they are now regular functions
    for func in module.functions.values():
        if "self" in func.parameters:
            parm = func.parameters._parameters_dict.pop("self")
            func.parameters._parameters_list.remove(parm)

    # extract prefixed members from the global namespace
    prefix = f"_{name}_"
    names = [n for n in root.members.keys() if n.startswith(prefix)]
    for member_name in names:
        member = root.members.pop(member_name)
        member.name = member_name[len(prefix) :]
        member.parent = module
        module.members[member.name] = member

    return module


SUBMODULE_PATTERN = """\
def __{name}() -> "HOM_{name} &":
    return _hou.__{name}()"""
"""The exact pattern we expect submodule-creator functions to look like."""


def is_submodule_func(func: Function) -> str:
    """Check if a function is a submodule creator.

    Returns the module name if it is a submodule. Otherwise returns an empty string
    """
    if not func.name.startswith("__"):
        return ""

    name = func.name[2:]
    pattern = SUBMODULE_PATTERN.format(name=name)
    return name if func.source == pattern else ""


def split_submodules(root: Module):
    """Split some classes into their own modules."""
    for func in root.functions.values():
        if name := is_submodule_func(func):
            _extract_module(root, name)
            root.members.pop(func.name)


################################################################################
# Processors for different object types
#
def process_type(name: str | Name | Expression | None) -> str:
    if not name:
        return ""
    name = str(name)
    name = cpp.parse(name)
    # parm.annotation = docstring.parse(parm.annotation)
    return name


def process_parameter(func: Function, parm: Parameter) -> None:

    # Convert "args=()" and "kwargs={}" to "*args: Any" and "**kwargs: Any"
    if parm.name == "args" and parm.default == "()":
        parm.name = "*args"
        parm.default = ""
        parm.annotation = "Any"
    if parm.name == "kwargs" and parm.default == "{}":
        parm.name = "**kwargs"
        parm.default = ""
        parm.annotation = "Any"

    if not parm.annotation:
        return
    # parse
    parm.annotation = process_type(parm.annotation)

    # convert annotations to absolute paths
    if parm.annotation in func.module.classes:
        parm.annotation = func.module.classes[parm.annotation].canonical_path

    # convert implicit_optional
    if parm.default == "None":
        parm.annotation = f"Optional[{parm.annotation}]"


def process_function(func: Function):

    for parameter in func.parameters:
        process_parameter(func, parameter)

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
        func.returns = process_type(func.returns)
        # func.returns = docstring.parse(func.returns)

    # auto Convert to classmethod
    is_method = func.parent and func.parent.is_class
    has_no_self = "self" not in func.parameters
    if is_method and has_no_self:
        decorator = "classmethod" if "cls" in func.parameters else "staticmethod"
        decorators = [d.value for d in func.decorators]  # make sure its not getting added twice
        if not decorator in decorators:
            func.decorators.append(Decorator(decorator, lineno=0, endlineno=0))


def add_enum_values(cls: Class) -> None:
    docstring = cls.docstring.value if cls.docstring else ""
    values = process_utils.enum_values_from_docstring(docstring)
    for name in values:
        # TODO: init with name once `__init__` methods are supported`
        cls.members[name] = Attribute(name=name, value=f"hou.EnumValue")


def process_class(cls: Class) -> None:
    cls.bases = [process_type(base) for base in cls.bases]
    add_enum_values(cls)


def process_module(module: Module) -> None:
    pass


def fix_top_level_function(attr: Attribute) -> None:
    """Replace calls to "__createTopLevelFunc(name)" with actual aliases."""

    pattern = r"__createTopLevelFunc\(\'(?P<name>\w+)\'\)"
    match = re.match(pattern, str(attr.value))
    if match:
        attr.value = f"houpythonportion.{match.group('name')}"


def process_attribute(attr: Attribute) -> None:
    fix_top_level_function(attr)


################################################################################


def process_object(obj: Object) -> Object:

    obj.members = {k: v for k, v in obj.members.items() if not skip_member(v)}

    # not sure if checking `.obj.KIND` would be besser.
    # but for now.. this plays better with myp
    if isinstance(obj, Module):
        process_module(obj)
    if isinstance(obj, Class):
        process_class(obj)
    if isinstance(obj, Function):
        process_function(obj)
    if isinstance(obj, Attribute):
        process_attribute(obj)

    for member in obj.members.values():
        if isinstance(member, Object):
            process_object(member)

    return obj
