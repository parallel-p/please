from . import test_info
import tempfile
import shutil

class FileTestInfo(test_info.TestInfo):
    def __init__(self, filename, tags={}):
        self.__file = filename
        self.__tags = tags
    
    def tests(self):
        temp = tempfile.NamedTemporaryFile(delete = False)
        shutil.copy(self.__file, temp.name)
        return [ temp.name ]
    
    def get_tags(self):
        return self.__attr
    
    def to_please_format(self):
        return get_to_please_format_prefix(self.__tags) + self.__file