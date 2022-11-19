
Usage:
----------------

```
hou_stubs/main.py /software_local/houdini-19.5/houdini/python3.9libs/hou.py
```



Todos:
----------------

* add `Any` for `args` and `kwargs`

* Tuple of Custom Classes need namespacing
  eg.: `_NodeTuple` -> `tuple[hou.Node]`

* fix bases for Classes
  eg.:
  ```py
  # this should be `hou.logging.Sink` or just `Sink`
  class FileSink(_logging_Sink):
    ...
  ```
