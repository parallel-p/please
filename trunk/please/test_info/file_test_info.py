from . import test_info
import tempfile
import shutil
#from ..well_done.well_done import WellDone

class FileTestInfo(test_info.TestInfo):
    def __init__(self, filename, tags={}, well_done=None):
        self.__file = filename
        self.__well_done = well_done
        super(FileTestInfo, self).__init__(tags)
    
    def tests(self):
        self.__well_done.check(self.__file)
        temp = tempfile.NamedTemporaryFile(delete = False)
        shutil.copy(self.__file, temp.name)
        return [ temp.name ]
    
    def to_please_format(self):
        return self.get_to_please_format_prefix() + self.__file