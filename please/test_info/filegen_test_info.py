from . import test_info

class FileGenTestInfo(test_info.TestInfo):
    def __init__(self, tags={}):
        super(FileTestInfo, self).__init__(tags)
        pass
    
    def tests(self):
        pass
    
    def to_please_format(self):
        pass 