import unittest
from please.language_configurator.python import get_python_configurator

class Tester (unittest.TestCase):

    def setUp(self):
        self.config = get_python_configurator ()

    def __run_tests (self,function,source,right_ans):
        self.assertEqual(function(source), right_ans)

    def test_PythonConfigurator (self):
        self.__run_tests(self.config.get_compile_command, "file_name", [""])

        self.__run_tests(self.config.get_run_command, "file_name.py", ["python", "-O", "file_name.py"])
        self.__run_tests(self.config.get_run_command, "C:\Programm files\file_name.py", ["python", "-O", "C:\Programm files\file_name.py"])

        self.__run_tests(self.config.is_run_garbage, "C:\Programm files\file_name.pyc", True)
        self.__run_tests(self.config.is_run_garbage, "C:\Programm files\file_name.py", False)
        self.__run_tests(self.config.is_run_garbage, "file_name.pyc",                   True)
        self.__run_tests(self.config.is_run_garbage, ".pyc",                           True)

if __name__ == "__main__":
    unittest.main()


