import please.language_configurator.cpp as lng_cpp

import unittest

class CppTest(unittest.TestCase):
    def test_win_compile(self):
        cpp = lng_cpp.CppWindowsConfigurator()
        out = cpp.get_compile_command("test.cpp")
        self.assertEqual(out, ["g++", "-lm", "-s", "-x", "c++", "-O2", "-o", "test.exe", "test.cpp"])
        
    def test_win_run(self):
        cpp = lng_cpp.CppWindowsConfigurator()
        out = cpp.get_run_command("abacaba.cpp")
        self.assertEqual(out, ["abacaba.exe"])
        
    def test_lin_compile(self):
        cpp = lng_cpp.CppLinuxConfigurator()
        out = cpp.get_compile_command("sample.cpp")
        self.assertEqual(out, ["g++", "-lm", "-s", "-x", "c++", "-O2", "-o", "sample", "sample.cpp"])
        
    def test_lin_run(self):
        cpp = lng_cpp.CppLinuxConfigurator()
        out = cpp.get_run_command("ololo.cpp")
        self.assertEqual(out, ["./ololo"])
        
    def test_lin_run2(self):
        cpp = lng_cpp.CppLinuxConfigurator()
        out = cpp.get_run_command("nice.bin")
        self.assertEqual(out, ["./nice"])
        
if __name__ == '__main__':
    unittest.main()
