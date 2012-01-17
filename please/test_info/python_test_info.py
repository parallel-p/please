from . import test_info
import tempfile

class PythonTestInfo(test_info.TestInfo):
    def __init__(self, code, modificator=None, tags={}, comment = ''):
        self.__code = code
        self.__modificator = modificator
        super(PythonTestInfo, self).__init__(tags, comment)
    
    def tests(self):
        temp = tempfile.NamedTemporaryFile(delete = False)
        try:
            with open(temp.name, 'w') as f:
                content = (lambda x : x if type(x) == str else '\n'.join(x))(eval(self.__code))
                if self.__modificator:
                    content = self.__modificator(content)
                f.write(content)
        except Exception as e:
            raise EnvironmentError(str(e))
        self.set_desc( ['python output'] )
        return [ temp.name ]
    
    def to_please_format(self):
        return ' '.join([seluf.get_prefix(), self.__code, self.get_suffix()]).strip()
