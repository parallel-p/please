from . import test_info
import tempfile

class EchoTestInfo(test_info.TestInfo):
    def __init__(self, line, tags={}):
        """
            example: line = "abacabadabacaba"
        """
        self.__line = str(line)
        super(EchoTestInfo, self).__init__(tags)
        
    def tests(self):
        stdout = tempfile.NamedTemporaryFile(delete = False)
        with open(stdout.name, 'w') as f:
            f.write(self.__line + '\n')
        
        return [stdout.name]
    
    def to_please_format(self):
        return self.get_to_please_format_prefix() + "echo " + self.__line