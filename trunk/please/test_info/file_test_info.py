from . import test_info
import tempfile
import shutil
import glob
from ..well_done import well_done

class FileTestInfo(test_info.TestInfo):
    def __init__(self, mask, tags={}, well_done=None):
        self.__mask = mask
        self.__well_done = well_done
        super(FileTestInfo, self).__init__(tags)
    
    def tests(self):
        result = []
        for file in glob.iglob(self.__mask):
            if self.__well_done is not None:
                self.__well_done.check(file)
            temp = tempfile.NamedTemporaryFile(delete = False)
            shutil.copy(file, temp.name)
            result.append(temp.name)
        return result
    
    def to_please_format(self):
        return self.get_to_please_format_prefix() + self.__file