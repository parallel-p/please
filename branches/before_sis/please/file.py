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
