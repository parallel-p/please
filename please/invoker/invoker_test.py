import unittest 
import os
import subprocess 

import psutil

from please.invoker.invoker import *
from please.utils.platform_detector import get_platform

class TestInvoker(unittest.TestCase):
    
    
    def setUp(self):
        platform = get_platform()
        self.TEST_FILE = os.path.join('please', 'invoker', 'test.') + platform[0][0].lower() + platform[1]
        #print(self.TEST_FILE)
        
    def tearDown(self):
        pass
            
            
    def test_invoker_ok_one_moment_program(self):
        for tries in range(1, 20):
            process = psutil.Popen([self.TEST_FILE, "0", "20"])
            limits = ExecutionLimits(real_time = 5.0, cpu_time = 5.0, memory = 200)  
            ret = invoke(process, limits)
            self.assertEqual(ret.verdict, "OK")
        
    def test_invoker_only_process_ok(self):
        for tries in range(1, 5):
            process = psutil.Popen([self.TEST_FILE, "1", "20"])
            limits = ExecutionLimits(real_time = 5.0, cpu_time = 5.0, memory = 200)  
            ret = invoke(process, limits)
            self.assertEqual(ret.verdict, "OK")
        

    def test_invoker_only_process_bad_tl(self):
        process = psutil.Popen([self.TEST_FILE, "2", "20"])
        limits = ExecutionLimits(real_time = 1, cpu_time = 1, memory = 200)
        ret = invoke(process, limits)
        self.assertEqual(ret.verdict, "real TL")

    def test_invoker_only_process_bad_ml(self):
        process = psutil.Popen([self.TEST_FILE, "1", "200"])
        limits = ExecutionLimits(real_time = 5, cpu_time = 5, memory = 50)  
        ret = invoke(process, limits)
        self.assertEqual(ret.verdict, "ML")

    def test_invoker_only_process_bad_re(self):
        process = psutil.Popen([self.TEST_FILE])
        limits = ExecutionLimits(real_time = 5, cpu_time = 5, memory = 50)  
        ret = invoke(process, limits)
        self.assertEqual(ret.verdict, "RE")

    def test_invoker_java_run_re(self):
        for iter in range(20):
            process = psutil.Popen(["java", "a"],
                stderr = subprocess.PIPE)
            limits = ExecutionLimits(real_time = 1, cpu_time = 1, memory = 50)  
            ret = invoke(process, limits)
            self.assertEqual(ret.verdict, "RE")

if __name__ == '__main__':
    unittest.main()
 
