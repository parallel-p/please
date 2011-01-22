class Validator:
    def __init__(self, file_system):
        self.__file_system = file_system

    def file(self):
        """Returns path to validator or None"""
        candidates = list(
            self.__file_system.find(".", "val.*\..*", deep = 2)
            )
        if len(candidates) != 1:
            return None
        else:
            return candidates[0]
