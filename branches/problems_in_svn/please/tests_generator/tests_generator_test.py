import shutil
import unittest, mox
import os
from please.tests_generator import tests_generator
from please.executors import runner, compiler
import io
from please.utils import line_ending

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

    def test_file(self):
        test_info = TestInfo("file", "file_path", {})
        test_info2 = TestInfo("file", "file_path2", {"second group"})

        self.mox.StubOutWithMock(os.path, "exists")
        os.path.exists(TESTS_DIR).MultipleTimes().AndReturn(True)

        self.mox.StubOutWithMock(shutil, "rmtree")
        shutil.rmtree(os.path.join(TESTS_DIR))

        self.mox.StubOutWithMock(shutil, "copyfile")
        shutil.copyfile("file_path2", os.path.join(TESTS_DIR, "2"))
        shutil.copyfile("file_path", os.path.join(TESTS_DIR, "1"))
        shutil.copyfile("file_path2", os.path.join(TESTS_DIR, "2"))
                
        self.mox.StubOutWithMock(line_ending, "convert")
        line_ending.convert(os.path.join(TESTS_DIR, "2"))
        line_ending.convert(os.path.join(TESTS_DIR, "1"))
        line_ending.convert(os.path.join(TESTS_DIR, "2"))

        self.mox.ReplayAll()
        
        test_generator = tests_generator.TestsGenerator([test_info, test_info2])
        test_generator.generate(lambda attributes : ("second group" in attributes))
        test_generator.generate_all()
        

    def test_generator_generate_all(self): 
        test_info = TestInfo("generator", ("file_path", [23, 23, 784]), {})
        test_info2 = TestInfo("generator", ("file_path2", []), {})
        
        self.mox.StubOutWithMock(os.path, "exists")
        os.path.exists(TESTS_DIR).MultipleTimes().AndReturn(False)

        #self.mox.StubOutWithMock(shutil, "rmtree")
        #shutil.rmtree(os.path.join(TESTS_DIR))
        
        self.mox.StubOutWithMock(os, "makedirs")
        os.makedirs(TESTS_DIR)

        self.mox.StubOutWithMock(compiler, "compile")
        compiler.compile(test_info.command[0])
        compiler.compile(test_info2.command[0])
        
        f1 = self.FileMock(self, "output1")
        f2 = self.FileMock(self, "output2")
        self.mox.StubOutWithMock(io, "open")
        io.open(os.path.join(TESTS_DIR, "1"), 'wb').AndReturn(f1)
        io.open(os.path.join(TESTS_DIR, "2"), 'wb').AndReturn(f2)

        self.mox.StubOutWithMock(runner, "run")
        runner.run(test_info.command[0], test_info.command[1]).AndReturn((None, "output1"))
        runner.run(test_info2.command[0], test_info2.command[1]).AndReturn((None, "output2"))
            
        #line_ending.convert(file_name)
        self.mox.StubOutWithMock(line_ending, "convert")
        line_ending.convert(os.path.join(TESTS_DIR, "1"))
        line_ending.convert(os.path.join(TESTS_DIR, "2"))

        self.mox.ReplayAll()
        
        test_generator = tests_generator.TestsGenerator([test_info, test_info2])
        test_generator.generate_all()

        self.assertTrue(f1.enter_called)
        self.assertTrue(f1.exit_called)
        self.assertTrue(f2.enter_called)
        self.assertTrue(f2.exit_called)
        
    def test_generator_generate(self): 
        test_info = TestInfo("generator", ("file_path0", [23, 23, 784]), {"sample"})
        test_info2 = TestInfo("generator", ("file_path02", []), {"third group"})
        
        self.mox.StubOutWithMock(os, "makedirs")
        os.makedirs(TESTS_DIR)

        self.mox.StubOutWithMock(compiler, "compile")
        compiler.compile(test_info.command[0])
        
        f1 = self.FileMock(self, "output1")
        self.mox.StubOutWithMock(io, "open")
        io.open(os.path.join(TESTS_DIR, "1"), 'wb').AndReturn(f1)

        self.mox.StubOutWithMock(runner, "run")
        runner.run(test_info.command[0], test_info.command[1]).AndReturn((None, "output1"))
        
        self.mox.StubOutWithMock(line_ending, "convert")
        line_ending.convert(os.path.join(TESTS_DIR, "1"))
    
        self.mox.ReplayAll()
        
        test_generator = tests_generator.TestsGenerator([test_info, test_info2])
        test_generator.generate(lambda attributes: ('sample' in attributes))

        self.assertTrue(f1.enter_called)
        self.assertTrue(f1.exit_called)

if __name__ == "__main__":
    unittest.main()
