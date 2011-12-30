from . import test_info

class CommandTestInfo(test_info.TestInfo):
    def __init__(self, command, args, tags={}):
        super(CommandTestInfo, self).__init__(tags)
        self.__command = command
        self.__args = args
    
    def tests(self):
        pass
    
    def to_please_format(self):
        pass 