# Houdini Stub File Generator

Type annotation builder for [SideFX Houdini](https://www.sidefx.com/) `hou`-python Module


## ⚠️ This project is no longer maintained.

> We recommend using 👉 [**LumaPictures/cg-stubs**](https://github.com/LumaPictures/cg-stubs) as a better alternative


## Usage:

1) run `main.py` to build the stub files
    ```bash
    $ hou_stubs/main.py "/path/to/your/houdini/19.5.303/houdini/python3.9libs/hou.py"

    # eg.:
    $ hou_stubs/main.py /software/houdini/19.5/houdini/python3.9libs/hou.py --out=./hou-stubs
    ```
2) include them in your `$PYTHONPATH`
    ```bash
    $ export PYTHONPATH="${PYTHONPATH}:/the/path/where/hou-stubs/is"
    ```

## Examples:

Error Checking:

![example error message](/docs/img/example1_error.png)

IDE Docs:

![example inline help](/docs/img/example2_ide_docs.png)

here is an example from the generated stubs:

![example stubs](/docs/img/example3_stub_file.png)


## Features:

#### Automatic splitting of Submodules:

![submodules](/docs/img/exmaple4_submodules.png)


## Nodes/Todo:

* Some C++ type are'nt 100% correct translated. In some cases I took shortcuts and
  and used similar behaving python types. eg.: pointers are just dropped.
  Different variations of Integer/Float/String types are all annoted as their basic `int`/`float`/`str`.

* The imports and namespaces in the submodules is a bit messy.
  Maybe its best to keep everything combined as one big module.

* `process.process_parameter` currently reads `func.module.classes` which takes a decent bit of time.
  Might be worth trying to optimize this. Maybe wrap the griffe-classes into our own
  sublclasses and make `classes()` a cached property

* Only the `hou.py` itself is supported/test.
 In theory the code should work fine on other modules, but its untested as of right now.

## Credits:

Large parts of the Code are inspired by [mypy-boto3-builder](https://github.com/youtype/mypy_boto3_builder).
