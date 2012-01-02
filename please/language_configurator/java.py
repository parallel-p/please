import os
import re
from .language_configurator_utils import is_windows

class JavaLinuxConfigurator:
    def get_compile_command(self, source):
        return ["javac", "-cp", ".;", source]

    def get_run_command(self, source):
        source_base_name = os.path.basename(source)
        source_name_without_ext = os.path.splitext(source_base_name)[0]
        source_dir = os.path.dirname(os.path.abspath(source))
        return ["java", "-cp", source_dir, source_name_without_ext]

    def get_binary_name(self, source):
        return [""]    
    
    def is_compile_garbage(self, source):
        return False

    def is_run_garbage(self, source):
        return False

JavaWindowsConfigurator = JavaLinuxConfigurator

def get_java_configurator():
    return JavaWindowsConfigurator() if is_windows() else JavaLinuxConfigurator()
