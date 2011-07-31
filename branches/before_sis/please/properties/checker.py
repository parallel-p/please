class Checker:
    TOKENS, INTEGERS, YES_NO = range(3)
    def __init__(self,
            file = None,
            standard_type = None
            ):
        if standard_type != None and file != None:
            raise Exception("checker must be either standard or in some file")
        self.__file = file
        self.__standard_type = standard_type

    def __checker_path_by_type(self, type):
        STANDARD_CHECKER_DIR = "standard_checkers_dir"
        import os.path
        return os.path.join(STANDARD_CHECKER_DIR, "checker.cpp")

    def file(self):
        if self.__standard_type != None:
            return self.__checker_path_by_type(self.__standard_type)
        else:
            return self.__file
