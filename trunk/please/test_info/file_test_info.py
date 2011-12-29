from . import test_info
import tempfile
import shutil

class FileTestInfo(test_info.TestInfo):
    def __init__(self, filename, tags={}):
        self.__file = filename
        super(FileTestInfo, self).__init__(tags)
    
    def tests(self):
        temp = tempfile.NamedTemporaryFile(delete = False)
        shutil.copy(self.__file, temp.name)
        return [ temp.name ]
    
    def to_please_format(self):
        return self.get_to_please_format_prefix() + self.__file