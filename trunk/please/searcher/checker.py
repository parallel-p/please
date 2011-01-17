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


if __name__ == "__main__":
    from mock import Mock
    import os.path

    for just_file in [os.path.join(dir, name + "." + ext)
            for dir in [".", "", "sources"]
            for name in ["check", "checker", "check_default"]
            for ext in ["cpp", "py", "pas", "dpr"]]:
        fs = Mock()
        fs.find = Mock(return_value = [just_file])
        assert(Checker(fs).file() == just_file)
