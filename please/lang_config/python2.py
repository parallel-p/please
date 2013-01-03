from .base import BaseConfig
from .utils import is_windows
import winreg
import sys
import itertools
import logging
import os
import glob, fnmatch

_logger = logging.getLogger('please_logger.lang_config.python2')

LANGUAGE = "python2"

exec_path = [os.path.normpath(p) for p in os.get_exec_path()]

def _find_py2_install_win():
    import winreg
    def _test_hkey(hkey):
        try:
            regkey = winreg.OpenKey(hkey, r'SOFTWARE\Python\Pythoncore')
        except WindowsError:
            return []
        versions = []
        for index in itertools.count():
            try:
                keyname = winreg.EnumKey(regkey, index)
            except WindowsError:
                break
            else:
                if not keyname.startswith('2.'):
                    continue
                with winreg.OpenKey(regkey, keyname) as verskey:
                    versions.append((keyname,
                                     os.path.normpath(winreg.QueryValue(verskey, 'InstallPath'))))
        return versions
    HKLM = winreg.HKEY_LOCAL_MACHINE
    HKCU = winreg.HKEY_CURRENT_USER
    everything = list(frozenset(_test_hkey(HKLM)) |
                      frozenset(_test_hkey(HKCU)))
    if not everything:
        okpaths = []
        for dir in exec_path:
            if os.path.isfile(os.path.join(dir, 'python.exe')):
                instpath = dir
                break
        else:
            instpath = None
    elif len(everything) == 1:
        instpath = everything[0][1]
    else:
        instpaths = []
        for item in everything:
            try:
                instpaths.append((exec_path.index(item[1]), item[1]))
            except ValueError:
                pass
        if not instpaths:
            everything.sort()
            instpath = everything[-1][1] # latest version
        else:
            if len(instpaths) > 1:
                instpaths.sort()
            instpath = inspaths[0][1] # first occurence in PATH

    if instpath is None:
        # last chance
        globs = glob.glob('C:\\Python2?\\python.exe')
        globs.sort()
        if globs:
            instpath = globs[-1] # latest version

    return instpath

def _find_py2_install_nix():
    import subprocess
    try:
        version = subprocess.check_output(['python', '-V'],
                                          stderr = subprocess.STDOUT)
    except OSError:
        pass
    else:
        # Most common case: everything is ok by default
        if version.startswith(b'Python 2.'):
            return 'python'

    # Now, check others
    found_pythons = []
    for dir in exec_path[1:]: # First one is already checked
        python = os.path.join(dir, 'python')
        if os.access(python, os.X_OK):
            found_pythons.append(python)

    found_py2s = []
    for i, python in enumerate(found_pythons):
        version = subprocess.check_output([python, '-V'],
                                         stderr = subprocess.STDOUT)
        version = version.decode('ascii')
        assert version.startswith('Python ')
        version = version[7:10]
        if version[0] == '2':
            found_py2s.append((version, -i, python))

    found_py2s.sort()
    if found_py2s:
        return found_py2s[-1][2]

    path_py2s = []
    # okay, not found; hard way
    for i, dir in enumerate(exec_path):
        for python2 in glob.iglob(os.path.join(dir, 'python2.?')):
            if os.access(python2, os.X_OK):
                path_py2s.append((os.path.basename(python2)[6:9],
                                  -i, python2))
    path_py2s.sort()
    if path_py2s:
        return path_py2s[-1][2]

    return None # sad, but true

if is_windows():
    instpath = _find_py2_install_win()
    if instpath is not None:
        executable = os.path.join(instpath, "python.exe")
    else:
        executable = None
else:
    executable = _find_py2_install_nix()
    

class Python2Config(BaseConfig):
    def _get_run_command(self, source):
        return [executable, '-O', source]

    def is_run_garbage(self, path):
        return path.endswith('.pyc')

    def _get_binaries(self, source):
        return []

def get_config():
    return Python2Config if executable is not None else None

