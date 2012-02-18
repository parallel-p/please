from . import test_info
from . import test_file_sort
from .test_file import FileTestFile
import os.path
import glob
#from ..well_done import well_done
import re


class FileTestInfo(test_info.TestInfo):
    def __init__(self, mask, tags={}, well_done=None, comment = ''):
        self.mask = mask
        self.__well_done = well_done
        self.exclude = re.compile(tags.get('exclude') or '$^')
        super(FileTestInfo, self).__init__(tags, comment)

    def __eq__(self, other):
        return (self.mask == other.mask and
                self.exclude.pattern == other.exclude.pattern)

    def __hash__(self):
        return hash(self.mask) ^ hash(self.exclude)
    
    def tests(self):
        result = []
        desc = []
        exclude = self.get_tags().get('exclude')
        files = []
        for file in glob.iglob(self.mask):
            if not self.exclude.match(file):
                files.append(FileTestFile(os.path.abspath(file), file))
        files.sort(key = test_file_sort.testfile_sorting_key)
        return files
    
    def to_please_format(self):
        return ' '.join([self.get_prefix(), self.mask, self.get_suffix()]).strip()
