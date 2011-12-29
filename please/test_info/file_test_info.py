from . import test_info
import tempfile
import shutil

class FileTestInfo(test_info.TestInfo):
    def __init__(filename, tags={}):
        self.__file = filename
        self.__tags = tags
    
    def tests():
        temp = tempfile.NamedTemporaryFile(delete = False)
        shutil.copy(self.__file, temp.name)
        return [ temp.name ]
    
    def get_tags():
        return self.__attr
    
    def to_please_format():
        return get_to_please_format_prefix(self.__tags) + self.__file