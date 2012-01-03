from . import test_info
import tempfile
import shutil
import glob
from ..well_done import well_done

class FileTestInfo(test_info.TestInfo):
    def __init__(self, mask, tags={}, well_done=None, comment = ''):
        self.__mask = mask
        self.__well_done = well_done
        super(FileTestInfo, self).__init__(tags, comment)
    
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
        return ' '.join([self.get_prefix(), self.__mask, self.get_suffix()]).strip()