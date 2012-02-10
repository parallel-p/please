from .language_configurator_utils import is_windows
import os

class CppLinuxConfigurator:
    def get_compile_command(self, source):
        return ["g++", "-lm", "-s", "-x", "c++",
        "-O2", "-o", os.path.splitext(source)[0], source]

    def get_run_command(self, source):
        if "/" not in source:
            source = "./" + source
        return [os.path.splitext(source)[0]]
    
    def get_binary_name (self, source):
        return [os.path.splitext(source)[0]]

    def is_compile_garbage(self, file):
        return False
    
    def is_run_garbage(self, file):
        return False

class CppWindowsConfigurator:
    def get_compile_command(self, source):
        return ["g++", "-lm", "-s", "-x", "c++",
        "-O2",
        "-o", os.path.splitext(source)[0] + ".exe",  source]
    
    def get_run_command(self, source):
        return [os.path.splitext(source)[0] + ".exe"]

    def get_binary_name (self, source):
        return [os.path.splitext(source)[0] + ".exe"]
    
    def is_compile_garbage(self, file):
        return False

    def is_run_garbage(self, file):
        return False

def get_cpp_configurator():
    ''' Returns configurator object depends on OS you run  '''
    return CppWindowsConfigurator() if is_windows() else CppLinuxConfigurator()
