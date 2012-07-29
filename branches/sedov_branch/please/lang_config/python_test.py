import unittest
from please.lang_config.python2 import get_config

class Tester (unittest.TestCase):

    def setUp(self):
        self.config = get_config()

    def __run_tests (self, attr, source, right_ans):
        self.assertEqual(getattr(self.config(source), attr), right_ans)

    def test_PythonConfigurator (self):
        self.__run_tests("compile_commands", 'test', ())

        self.__run_tests("run_command", "file_name.py", ["python", "-O", "file_name.py"])
        self.__run_tests("run_command", "C:\\Programm files\\file_name.py", ["python", "-O", "C:\\Programm files\\file_name.py"])

        config = self.config("file_name.py")
        is_garbage = config.is_run_garbage
        self.assertTrue(is_garbage("C:\Programm files\file_name.pyc"))
        self.assertFalse(is_garbage("C:\Programm files\file_name.py"))
        self.assertTrue(is_garbage("file_name.pyc"))
        self.assertTrue(is_garbage(".pyc"))

if __name__ == "__main__":
    unittest.main()


