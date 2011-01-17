#!/usr/bin/python

import os
import os.path

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
            os.path.normpath(
                os.path.join(search_dir, file)) for
            file in os.listdir(search_dir)
            if func_filter(os.path.join(search_dir, file))]

    def files(self, subdir):
        return self.__items(
            os.path.join(self.__pwd, subdir),
            os.path.isfile)

    def dirs(self, subdir):
        return self.__items(
            os.path.join(self.__pwd, subdir),
            os.path.isdir)

if __name__ == "__main__":
    fs = FileSystem()
    print(list(fs.files(".")))
    print(list(fs.dirs(".")))
    print(list(fs.files("commands")))
