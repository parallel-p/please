class Validator:
    def __init__(self, file = None,
            input = "stdin", output = "stdout"):
        self.__file = file
        self.__input = input
        self.__output = output

    def file(self):
        return self.__file

    def input(self):
        return self.__input

    def output(self):
        return self.__output
