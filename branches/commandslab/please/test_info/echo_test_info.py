from . import test_info
import tempfile
from .test_file import StrTestFile
class EchoTestInfo(test_info.TestInfo):
    def __init__(self, line, tags={}, comment = ''):
        """
            example: line = "abacabadabacaba"
        """
        self.testfile = StrTestFile(str(line) + '\n', 'echo output')
        self.line = str(line)
        super().__init__(tags, comment)
        
    def tests(self):
        return [self.testfile]

    def __eq__(self, other):
        return self.line == other.line

    def __hash__(self):
        return hash(self.line)
    
    def to_please_format(self):
        return ' '.join([self.get_prefix(), "echo", self.line, self.get_suffix()]).strip()
