import sys
import typing
from dataclasses import dataclass

import pytest

from hou_stubs.render import get_module_filename


@dataclass
class FakeModule:
    canonical_path: str
    modules: bool


if typing.TYPE_CHECKING:
    from griffe.dataclasses import Module
else:
    Module = FakeModule


def test__get_module_filename__root():
    module = Module("foo", modules=True)
    assert get_module_filename(module) == "foo-stubs/__init__.pyi"


def test__get_module_filename__nosubmodules():
    module = Module("foo", modules=False)
    assert get_module_filename(module) == "foo.pyi"


def test__get_module_filename__child():
    module = Module("foo.bar.baz", modules=False)
    assert get_module_filename(module) == "foo-stubs/bar/baz.pyi"


if __name__ == "__main__":
    pytest.main(sys.argv)
