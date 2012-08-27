import sys
import os

def is_windows():
    return sys.platform.startswith('win')

PATH = os.get_exec_path()

if is_windows() or os.path.__name__ == 'ntpath':
    exe_suffix = '.exe'
    def run_command(name):
        return os.path.splitext(name)[0] + exe_suffix
else:
    exe_suffix = ''
    def run_command(name):
        name = os.path.splitext(name)[0]
        if os.sep not in name:
            return os.path.join(os.curdir, name)
        return name

def exists(name):
    if os.sep in name:
        variants = [name]
    else:
        variants = [os.path.join(dir, name) for dir in PATH]
    for path in variants:
        if os.path.isfile(path) or os.path.isfile(path + exe_suffix):
            return True
    return False

def choose(*classes):
    for class_ in classes:
        if class_.requirements:
            return class_
    raise OSError('No alternatives found')
