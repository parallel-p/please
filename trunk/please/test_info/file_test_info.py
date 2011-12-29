from . import test_info
import tempfile
import shutil

class FileTestInfo(test_info.TestInfo):
    def __init__(filename, tags={}):
        self.__file = filename
        self.__tags = tags
    
    def tests():
        temp = tempfile.NamedTemporaryFile(delete = False)
        shutil.copy(self.__file, temp.name)
        return [ temp.name ]
    
    def get_tags():
        return self.__attr
    
    def to_please_format():
        tags_list = []
        for key, value in self.__tags.items():
            curtag = str(key)
            if value is not None:
                curtag += " = " + str(value)
            tags_list.append(curtag)
        return "[" + ', '.join(tags_list) + "] " + self.__file