import os
import sys
from unittest import mock

os.environ["HOUDINI_QT_PREFERRED_BINDING"] = "PySide2"


sys.path.append("/software/houdini-19.5/houdini/python3.9libs")
sys.path.append("/software/houdini-19.5/python/lib/python3.9/site-packages")
sys.path.append("/software/houdini-19.5/python/lib/python3.9/site-packages-forced")


sys.modules["_hou"] = mock.MagicMock()
# sys.modules["future"] = mock.Mock()

sys.modules["_hwebserver"] = mock.MagicMock()
sys.modules["_hwebserver"].PyWebSocket = mock.Mock()
sys.modules["_hwebserver"].PyURLHandler = mock.Mock()


sys.modules["hutil.Qt"] = mock.MagicMock()
sys.modules["_houqt"] = mock.MagicMock()
# mock.patch("QtWidgets").start()
# mock.patch("QtWidgets.QApplication.style").start()
# QtWidgets.QApplication.style()
