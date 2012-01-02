from . import test_info
import tempfile

class TestConfigParserError(Exception):
    pass

class PythonTestInfo(test_info.TestInfo):
    def __init__(self, code, tags={}):
        self.__code = code
        super(PythonTestInfo, self).__init__(tags)
    
    def tests(self):
        temp = tempfile.NamedTemporaryFile(delete = False)
        try:
            with open(temp.name, 'w') as f:
                f.write(str(eval(self.__code)))
        except Exception as e:
            raise TestConfigParserError(str(e))
        return [ temp.name ]
    
    def to_please_format(self):
        return self.get_to_please_format_prefix() + self.__code