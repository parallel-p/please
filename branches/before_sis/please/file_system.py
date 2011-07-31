#!/usr/bin/python

import os
import re
import shutil

class FileSystem:
    """
    This class done to mock it on tests and possible
    we will store files not only on disk (on DB? directly in svn?
    looking forward for svn server and web server...)
    """
    def __init__(self, pwd = "."):
        self.__pwd = pwd

    def __items(self, search_dir, func_filter):
        return [
            os.path.relpath(os.path.join(search_dir, file),
                self.__pwd)
            for file in os.listdir(search_dir)
            if func_filter(os.path.join(search_dir, file))]

    def root(self):
        return self.__pwd
    
    def root_basename(self):
        return os.path.basename(self.__pwd)
    
    def exists(self, file):
        return os.path.exists(os.path.join(self.__pwd, file))

    def read(self, file):
        with open(os.path.join(self.__pwd, file), "rt") as f:
            return f.read()

    def files(self, subdir):
        return self.__items(
            os.path.join(self.__pwd, subdir),
            os.path.isfile)

    def dirs(self, subdir):
        return self.__items(
            os.path.join(self.__pwd, subdir),
            os.path.isdir)

    def find(self, subdir, basename_regex, depth = 1):
        """generator of all files accepted by regex"""
        for file in self.files(subdir):
            if re.search(basename_regex, os.path.basename(file)):
                yield file
        if depth > 1:
            for dir in self.dirs(subdir):
                if not dir.startswith("."):
                    for file in self.find(dir, basename_regex, depth - 1):
                        yield file
    
    def del_dir(self, dir):
        if self.exists(dir):
            shutil.rmtree(dir)
    
    def mkdir(self, dir):
        os.makedirs(dir)
        
    def exec(self, command, args,  localRun = False):
        if localRun and (os.name == "posix"):
            command = os.path.join(".", command)
        os.system(command + " " + args)
        
    def copy(self, file1, file2):
        shutil.copy(file1, file2)
        
    def echoToFile(self,  fname, contents):
        f = open(fname, "w")
        f.write(contents)
        f.close()
        
    def chdir(self, dir):
        self.__pwd = os.path.abspath(dir) #Is anything else needed?
        os.chdir(dir)
    
    def binarySuffix(self):
        if os.name == "posix": 
            return ""
        elif os.name == "nt": 
            return ".exe"

if __name__ == "__main__":
    fs = FileSystem()
    print(list(fs.files(".")))
    print(list(fs.dirs(".")))
    print(list(fs.files("commands")))
    print("finding...")
    print(list(fs.find(".", ".*\.py")))
    print(list(fs.find(".", ".*\.py", depth = 1)))
    print(list(fs.find(".", ".*\.py", depth = 2)))
    print(list(fs.find("commands", ".*\.py", depth = 2)))
    assert(fs.exists("__init__.py"))
    assert(fs.exists(os.path.join("extensions", "base.py")))

