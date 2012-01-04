import os
import re
from .language_configurator_utils import is_windows
import glob

#TODO: get from global config
COMPILE_DIR = ".please"

class JavaLinuxConfigurator:
    def __class_file(self, source):
        return os.path.splitext(os.path.basename(source))[0]

    def __source_dir(self, source):
        return os.path.dirname(source)

    def get_compile_command(self, source):
        source_dir = self.__source_dir(source)
        if source_dir: source_dir = ';' + source_dir
        return ["javac", "-d", COMPILE_DIR, "-cp", ".%s" % source_dir, source]

    def get_run_command(self, source):
        class_file = self.__class_file(source)
        return ["java", "-cp", COMPILE_DIR, class_file]

    def get_binary_name(self, source):
        class_file = self.__class_file(source)
        binaries = set()
        run_binary = os.path.join(COMPILE_DIR, "%s.class") % class_file
        binaries = list(glob.glob(os.path.join(COMPILE_DIR, "*.class")))
        if run_binary not in binaries:
            binaries += [run_binary]
        return binaries
 
    def is_compile_garbage(self, source):
        return False

    def is_run_garbage(self, source):
        return False

JavaWindowsConfigurator = JavaLinuxConfigurator

def get_java_configurator():
    return JavaWindowsConfigurator() if is_windows() else JavaLinuxConfigurator()
