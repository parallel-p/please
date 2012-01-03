from . import test_info
import tempfile
import logging
logger = logging.getLogger("please_logger.test_info.python_test_info")
class PythonTestInfo(test_info.TestInfo):
    def __init__(self, code, tags={}, comment = ''):
        self.__code = code
        super(PythonTestInfo, self).__init__(tags, comment)
    
    def tests(self):
        temp = tempfile.NamedTemporaryFile(delete = False)
        try:
            with open(temp.name, 'w') as f:
                f.write(str(eval(self.__code)))
        except Exception as e:
            raise EnvironmentError(str(e))
        logger.info("Python-result file is generated")
        return [ temp.name ]
    
    def to_please_format(self):
        return ' '.join([self.get_prefix(), self.__code, self.get_suffix()]).strip()