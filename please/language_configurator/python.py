from .language_configurator_utils import is_windows

class PythonConfigurator:
    def get_compile_command(self, source):
        return [""]

    def get_run_command(self, source):
        return ["python", "-O", source]
    
    def get_binary_name(self, source):
        return [""]

    def is_run_garbage(self, path):
        return path.endswith(".pyc")

    def is_compile_garbage (self, path) :
        return False

class Python3LinuxConfigurator:
    def get_compile_command(self, source):
        return [""]

    def get_run_command(self, source):
        return ["python3", "-O", source]
    
    def get_binary_name(self, source):
        return [""]

    def is_run_garbage(self, path):
        return path.endswith(".pyc")

    def is_compile_garbage (self, path) :
        return False

def get_python_configurator():
    return PythonConfigurator()

def get_python3_configurator():
    return PythonConfigurator() if is_windows() else Python3LinuxConfigurator()
