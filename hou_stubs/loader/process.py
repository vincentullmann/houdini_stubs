from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import re

# IMPORT THIRD PARTY LIBRARIES
from griffe.dataclasses import Alias, Class, Decorator, Function, Module, Object, Parameter

# IMPORT LOCAL LIBRARIES
from hou_stubs.parser import cpp, docstring

BLACKLIST = [
    "SwigPyIterator",
    "thisown",
    "options",
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

    # if name.startswith("_"):
    #     return True

    # all the "_FooTuple" Classes
    if re.match(r"_(.+)Tuple", name):
        return True

    if name in BLACKLIST:
        return True

    return False


def _extract_module(root: Module, name: str) -> Module | None:
    # modules.append(module)
    # module.kind = Kind.MODULE
    try:
        source = root.members.pop(name)
    except KeyError:
        return None

    module = Module(name=name)
    module.parent = root
    module.members = source.members
    root.members[name] = module

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
        member.name = member_name[1:].replace("_", ".")
        member.parent = module
        print("member.name", member.name)
        module.members[member.name] = member

    return module


def split_submodules(root: Module, *submodules: str) -> list[Module]:
    """Split some classes into their own modules."""

    modules: list[Module] = [root]
    for name in submodules:
        module = _extract_module(root, name)
        if module:
            modules.append(module)
        # if module:
        #     root[name] = module

    return modules


def process_parameter(parm: Parameter):
    if parm.annotation:
        parm.annotation = str(parm.annotation)
        parm.annotation = cpp.parse(parm.annotation)
        parm.annotation = docstring.parse(parm.annotation)

        if parm.default == "None":
            parm.annotation = f"Optional[{parm.annotation}]"

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
        func.returns = str(func.returns)
        func.returns = cpp.parse(func.returns)
        func.returns = docstring.parse(func.returns)

    # auto Convert to classmethod
    is_method = func.parent and func.parent.is_class
    has_no_self = "self" not in func.parameters
    if is_method and has_no_self:
        decorator = "classmethod" if "cls" in func.parameters else "staticmethod"
        decorators = [d.value for d in func.decorators]  # make sure its not getting added twice
        if not decorator in decorators:
            func.decorators.append(Decorator(decorator, lineno=0, endlineno=0))


def process_class(cls: Class) -> None:
    cls.name = remove_prefix(cls.name, f"{cls.module.name}.")
    cls.name = remove_prefix(cls.name, f"hou.{cls.module.name}.")


def process_module(module: Module):
    pass


def process_object(obj: Object):

    obj.members = {k: v for k, v in obj.members.items() if not skip_member(v)}

    # not sure if checking `.obj.KIND` would be besser.
    # but for now.. this plays better with myp
    if isinstance(obj, Module):
        process_module(obj)
    if isinstance(obj, Class):
        process_class(obj)
    if isinstance(obj, Function):
        process_function(obj)

    for member in obj.members.values():
        if isinstance(member, Object):
            process_object(member)

    return obj
