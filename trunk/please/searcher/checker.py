#TODO: push programs extension here to find only programs
class Checker:
    def __init__(self, file_system):
        self.__file_system = file_system

    def file(self):
        """Returns path to checker or None"""
        candidates = list(
            self.__file_system.find(".", "check.*\..*", deep = 2)
            )
        if len(candidates) != 1:
            return None
        else:
            return candidates[0]
