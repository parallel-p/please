import os
import os.path
from   .language_configurator_utils import is_windows

def is_compilation_garbage(source):

    extensions = [".bpg", ".bpl", ".cfg", ".dcp", ".dcu",
        ".ddp", ".dfm", ".~df", ".dof", ".dpk", ".~dp", ".dsk",
        ".dsm", ".dci", ".dro", ".dmt", ".dct", ".obj", ".~pa",
        ".res", ".rc", ".todo", ".o", ".bak"]

    if os.path.splitext(source)[1] == '':
        return False

    extension = os.path.splitext(source)[1]
    return extension.lower() in extensions

def is_running_garbage (source): #no garbage after running dpr project
    return False

class DprLinuxConfigurator:

    def get_compile_command(self, source):
        return ["fpc", source]

    def get_run_command(self, source):
        if "/" not in source:
            source = "./" + source
        return [os.path.splitext(source)[0]]
    
    def get_binary_name(self, source):
        return [os.path.splitext(source)[0]]

    def is_compile_garbage (self, source) :
        return is_compilation_garbage(source)

    def is_run_garbage (self, source) :
        return is_running_garbage(source)


class DprWindowsConfigurator:

    def get_compile_command(self, source):
        return ["dcc32.exe", "-cc", source]

    def get_run_command(self, source):
        return [os.path.splitext(source)[0] + ".exe"]
    
    def get_binary_name(self, source):
        return [os.path.splitext(source)[0] + ".exe"]

    def is_compile_garbage (self, source) :
        return is_compilation_garbage(source)

    def is_run_garbage (self, source) :
        return is_running_garbage (source)


def get_dpr_configurator():
    return DprWindowsConfigurator() if is_windows() else DprLinuxConfigurator()

