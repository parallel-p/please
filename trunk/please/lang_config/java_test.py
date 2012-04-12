import please.lang_config.java as javaconf
import os
import unittest

class JavaTest(unittest.TestCase):
    #def test_win_compile(self):
    #    java = javaconf.JavaWindowsConfigurator()
    #    out = java.get_compile_command("test.java")
    #    self.assertEqual(out, ["javac", "-d", os.path.join(".please", "test.java_javac"), "-cp", ".", "test.java"])
    #    
    #def test_win_run1(self):
    #    java = javaconf.JavaWindowsConfigurator()
    #    out = java.get_run_command("abacaba.java")
    #    self.assertEqual(out, ["java", "-cp", os.path.join(".please", "abacaba.java_javac"), "abacaba"])
    #    
    #def test_win_run2(self):
    #    java = javaconf.JavaWindowsConfigurator()
    #    out = java.get_run_command("aba/caba.java")
    #    self.assertEqual(out, ["java", "-cp", os.path.join(".please", "caba.java_javac"), "caba"])
    # Windows is the same as Linux is!

    def test_compile(self):
        java = javaconf.JavaConfig('test.java')
        self.assertEqual(java.compile_commands, (["javac" ,"-d",
                                                  os.path.join(".please", "test.java_javac"),
                                                  "-cp", ".", "test.java"],))
        
    def test_run(self):
        java = javaconf.JavaConfig('abacaba.java')
        self.assertEqual(java.run_command, ["java", "-Xmx1G", "-Xss64M", "-cp",
                                            os.path.join(".please", "abacaba.java_javac"),
                                            "abacaba"])
        
    def test_run2(self):
        java = javaconf.JavaConfig('aba/caba.java')
        self.assertEqual(java.run_command, ["java", "-Xmx1G", "-Xss64M", "-cp",
                                            os.path.join(".please", "caba.java_javac"),
                                            "caba"])

    #TODO: add tests for is_compile_garbage and get_binary_name
    #TODO: add tests for compiling in another dir
        
if __name__ == '__main__':
    unittest.main()
