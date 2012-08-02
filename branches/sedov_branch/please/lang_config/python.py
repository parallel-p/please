from . import python2, python3
import logging
import os
logger = logging.getLogger("please_logger.lang_config.python")

LANGUAGE = "python"
MIMES = ["x-python"]
EXTENSIONS = ["py"]

_py2warning = set()
_py2config = python2.get_config()
_py3config = python3.get_config()

def PythonConfig(path):
    path_handle = os.path.realpath(path)
    with open(path, 'rb') as f:
        line = f.readline()
    if b"python3" in line:
        return _py3config(path)
    elif b"python2" in line:
        return _py2config(path)
    elif path_handle in _py2warning:
        return _py2config(path)
    else:
        logger.warning("Assuming " + path + " is python2 file. \nIf you want to translate it with python3, insert 'python3' in the comment in the first line of this file")
        _py2warning.add(path_handle)
        return _py2config(path)

def get_config():
    return PythonConfig
