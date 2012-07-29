from . import test_info
from ..utils.exceptions import PleaseException
from .test_file import StrTestFile

def convert_content_to_string(content):
    if type(content) == list:
        return "\n".join([convert_content_to_string(x) for x in content])
    return str(content)

class PythonTestInfo(test_info.TestInfo):
    def __init__(self, code, modificator=None, tags={}, comment = ''):
        self.__code = compile(code, '<python test>', 'eval')
        self.__modificator = modificator
        super(PythonTestInfo, self).__init__(tags, comment)

    def tests(self):
        try:
            content = convert_content_to_string(eval(self.__code, {}, {}))
            if self.__modificator:
                content = self.__modificator(content)
            return [StrTestFile(content, 'python output')]
        except Exception as e:
            raise PleaseException(
                "Python test generator `%s` failed with exception: `%s`" % (self.__code, e))
    
    def to_please_format(self):
        return ' '.join([self.get_prefix(), self.__code, self.get_suffix()]).strip()
