import unittest

from please.language_configurator.dpr import DprLinuxConfigurator, DprWindowsConfigurator
from please.language_configurator.cpp import CppLinuxConfigurator, CppWindowsConfigurator
from please.language_configurator.python import PythonConfigurator
from please.language_configurator.java import JavaLinuxConfigurator, JavaWindowsConfigurator

class ModuleIntefaceTest(unittest.TestCase):    
    def test_same_methods(self) :        
        for language_class in [DprLinuxConfigurator(), DprWindowsConfigurator(), 
                               CppLinuxConfigurator(), CppWindowsConfigurator(), 
                               PythonConfigurator (), JavaLinuxConfigurator(), JavaWindowsConfigurator ()] :
            for method in ["get_compile_command", "get_run_command", "is_compile_garbage", "is_run_garbage"] :
                self.assertTrue(method in dir(language_class))
    
if __name__ == '__main__':
    unittest.main()
                                             
                 



