from . import cpp as lng_cpp

import unittest

class CppTest(unittest.TestCase):
    def test_win_compile(self):
        cpp = lng_cpp.CppWindowsConfig('test.cpp')
        self.assertEqual(cpp.compile_commands,
                         (["g++", "-lm", "-s", "-x", "c++", "-O2",
                           "-o", "test.exe", "test.cpp"],))
        
    def test_win_run(self):
        cpp = lng_cpp.CppWindowsConfig('abacaba.cpp')
        self.assertEqual(cpp.run_command, ["abacaba.exe"])
        
    def test_lin_compile(self):
        cpp = lng_cpp.CppNixConfig("sample.cpp")
        self.assertEqual(cpp.compile_commands, (["g++", "-lm", "-s", "-x", "c++", "-O2",
                                                 "-o", "sample", "sample.cpp"],))
        
    def test_lin_run(self):
        cpp = lng_cpp.CppNixConfig("ololo.cpp")
        self.assertEqual(cpp.run_command, ["./ololo"])
        
    def test_lin_run2(self):
        cpp = lng_cpp.CppNixConfig("nice.bin")
        self.assertEqual(cpp.run_command, ["./nice"])
        
if __name__ == '__main__':
    unittest.main()
