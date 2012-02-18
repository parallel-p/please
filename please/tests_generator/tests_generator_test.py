import shutil
import unittest, mox
import os
from please.tests_generator import tests_generator
import io
from please.utils import line_ending
from please.test_info.test_file import FileTestFile

TESTS_DIR = ".tests"

class TestInfo():
    def __init__(self, _type, _command, attributes):
        self.attributes = attributes
        self.type = _type
        self.command = _command
        
class Tester(unittest.TestCase):
    
    def setUp(self):
        self.mox = mox.Mox()
    
    def tearDown(self):
        self.mox.UnsetStubs()
        self.mox.VerifyAll()
        
    class FileMock():
        def __init__(self, test, expected_write):
            self.test = test
            self.expected_write = expected_write
            self.enter_called = False
            self.exit_called = False
        def __exit__(self, unused_arg1, unused_arg2, unused_arg3):
            self.exit_called = True
        def __enter__(self):
            self.enter_called = True
        def write(self, data):
            self.test.assertEqual(self.expected_write, data)
            
    class TestInfoMock():
        def __init__(self, filename, tags, new_filename, desc):
            self.file = filename
            self.__tags = tags
            self.__new_filename = new_filename
            self.__desc = desc
        def get_tags(self):
            return self.__tags
        def tests(self):
            return [FileTestFile(self.__new_filename, self.__desc)]
            

    def test_file(self):
        
        test_info = self.TestInfoMock("file_path", set(), "new_file_path", "file_path")
        test_info2 = self.TestInfoMock("file_path2", {"second group"}, "new_file_path2", "file_path2")
        
        self.mox.StubOutWithMock(os.path, "exists")
        os.path.exists(TESTS_DIR).MultipleTimes().AndReturn(True)

        self.mox.StubOutWithMock(shutil, "rmtree")
        shutil.rmtree(os.path.join(TESTS_DIR)).MultipleTimes()

        self.mox.StubOutWithMock(shutil, "copy")
        self.mox.StubOutWithMock(line_ending, "convert")
        shutil.copy("new_file_path2", os.path.join(TESTS_DIR, "1"))
        line_ending.convert(os.path.join(TESTS_DIR, "1"))
        shutil.copy("new_file_path", os.path.join(TESTS_DIR, "1"))
        line_ending.convert(os.path.join(TESTS_DIR, "1"))
        shutil.copy("new_file_path2", os.path.join(TESTS_DIR, "2"))
        line_ending.convert(os.path.join(TESTS_DIR, "2"))

        self.mox.ReplayAll()
        
        test_generator = tests_generator.TestsGenerator([test_info, test_info2])
        test_generator.generate(lambda tags : ("second group" in tags))
        test_generator.generate_all()

if __name__ == "__main__":
    unittest.main()

