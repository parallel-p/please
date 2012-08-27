import os
from .utils import is_windows
import glob
from .base import BaseConfig

LANGUAGE = "java"
MIMES = ["text/x-java"]
EXTENSIONS = [".java"]

class JavaConfig(BaseConfig):
    def __class_file(self, source):
        return os.path.splitext(os.path.basename(source))[0]

    def __source_dir(self, source):
        return os.path.dirname(source)

    def __compile_dir(self, source):
        #TODO: move to global config
        COMPILE_DIR = ".please"
        return os.path.join(COMPILE_DIR, os.path.basename(source) + "_javac")

    def _get_compile_commands(self, source):
        source_dir = self.__source_dir(source)
        if source_dir: source_dir = ';' + source_dir
        compile_dir = self.__compile_dir(source)
        #create directory for this java file
        if not os.path.exists(compile_dir):
            #TODO: think about where is better to create directory
            os.makedirs(compile_dir)
        return (["javac", "-d", compile_dir, "-cp", ".%s" % source_dir, source], )

    def _get_run_command(self, source):
        class_file = self.__class_file(source)
        return ["java", "-Xmx1G", "-Xss64M", "-cp", self.__compile_dir(source), class_file]

    def _get_binaries(self, source):
        class_file = self.__class_file(source)
        binaries = set()
        #we return all .class files from 
        compile_dir = self.__compile_dir(source)
        run_binary = os.path.join(compile_dir, "%s.class") % class_file
        binaries = list(glob.glob(os.path.join(compile_dir, "*.class")))
        if run_binary not in binaries:
            binaries += [run_binary]
        return binaries
 
def get_config():
    return JavaConfig
