import please.language_configurator.java as javaconf
import os
import unittest

class JavaTest(unittest.TestCase):
    def test_win_compile(self):
        java = javaconf.JavaWindowsConfigurator()
        out = java.get_compile_command("test.java")
        self.assertEqual(out, ["javac", "-cp", ".;", "test.java"])
        
    def test_win_run1(self):
        java = javaconf.JavaWindowsConfigurator()
        out = java.get_run_command("abacaba.java")
        self.assertEqual(out, ["java", "-cp", os.path.dirname(os.path.abspath("abacaba")) ,"abacaba"])
        
    def test_win_run2(self):
        java = javaconf.JavaWindowsConfigurator()
        out = java.get_run_command("aba/caba.java")
        self.assertEqual(out, ["java", "-cp", os.path.dirname(os.path.abspath("aba/caba")), "caba"])
        
    def test_linux_compile(self):
        java = javaconf.JavaLinuxConfigurator()
        out = java.get_compile_command("test.java")
        self.assertEqual(out, ["javac" ,"-cp", ".;", "test.java"])
        
    def test_linux_run(self):
        java = javaconf.JavaLinuxConfigurator()
        out = java.get_run_command("abacaba.java")
        self.assertEqual(out, ["java", "-cp", os.path.dirname(os.path.abspath("abacaba")),"abacaba"])
        
    def test_linux_run2(self):
        java = javaconf.JavaLinuxConfigurator()
        out = java.get_run_command("aba/caba.java")
        self.assertEqual(out, ["java", "-cp", os.path.dirname(os.path.abspath("aba/caba")), "caba"])
        
if __name__ == '__main__':
    unittest.main()
