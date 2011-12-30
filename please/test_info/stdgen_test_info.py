from . import test_info

class StdGenTestInfo(test_info.TestInfo):
    def __init__(self, generator, args, tags={}):
        super(FileTestInfo, self).__init__(tags)
        self.__generator = generator
        self.__args = args
        
    def tests(self):
        pass
    
    def to_please_format(self):
        pass 