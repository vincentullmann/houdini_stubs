
Usage:
----------------

```
hou_stubs/main.py /software_local/houdini-19.5/houdini/python3.9libs/hou.py
```


Todo:
----------------

* `process.process_parameter` currently reads `func.module.classes` which takes a decent bit of time.
  Might be worth trying to optimize this. Maybe wrap the griffe-classes into our own
  sublclasses and make `classes()` a cached property
