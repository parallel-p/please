from . import test_info
import tempfile
import shutil
import glob
from ..well_done import well_done
import re

class FileTestInfo(test_info.TestInfo):
    def __init__(self, mask, tags={}, well_done=None, comment = ''):
        self.__mask = mask
        self.__well_done = well_done
        super(FileTestInfo, self).__init__(tags, comment)
    
    def tests(self):
        result = []
        desc = []
        exclude = self.get_tags().get('exclude')
        for file in glob.iglob(self.__mask):
            if exclude is not None:
                if re.match(exclude, file) is not None:
                    continue
            if self.__well_done is not None:
                self.__well_done.check(file)
            temp = tempfile.NamedTemporaryFile(delete = False)
            shutil.copy(file, temp.name)
            result.append(temp.name)
            desc.append(file)
        self.set_desc(desc)
        return result
    
    def to_please_format(self):
        return ' '.join([self.get_prefix(), self.__mask, self.get_suffix()]).strip()