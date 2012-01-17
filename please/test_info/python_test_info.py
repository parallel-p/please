from ..executors import runner
from . import test_info
import tempfile

def convert_content_to_string(content):
    if type(content) == list:
        return "\n".join([convert_content_to_string(x) for x in content])
    return str(content)

class PythonTestInfo(test_info.TestInfo):
    def __init__(self, code, modificator=None, tags={}, comment = ''):
        self.__code = code
        self.__modificator = modificator
        super(PythonTestInfo, self).__init__(tags, comment)

    def tests(self):
        temp = tempfile.NamedTemporaryFile(delete = False)
        try:
            with open(temp.name, 'w') as f:
                content = convert_content_to_string(eval(self.__code))
                if self.__modificator:
                    content = self.__modificator(content)
                f.write(content)
        except Exception as e:
            raise runner.RunnerError(
                "python test generator `%s` failed with exception: `%s`" % (self.__code, e))
        self.set_desc( ['python output'] )
        return [ temp.name ]
    
    def to_please_format(self):
        return ' '.join([seluf.get_prefix(), self.__code, self.get_suffix()]).strip()
