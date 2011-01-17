#!/usr/bin/python

import os
import os.path

class File:
    """
    Helpful utility for working with files
    """
    
    def __init__(self, filename):
        self.__filename = filename

    def basename(self):
        return os.path.basename(self.__filename)

    def extension(self):
        extension_split = self.basename().rsplit(".", 1)
        if len(extension_split) == 1:
            return ""
        else:
            return extension_split[1]

if __name__ == "__main__":
    for filename, extension, basename in [
            ("./ura.php", "php", "ura.php"),
            ("././dere/.svn/ura.cpp", "cpp", "ura.cpp"),
            ("ewr/ura", "", "ura")]:
        f = File(filename)
        assert(f.extension() == extension)
        assert(f.basename() == basename)
