import unittest
import os
from please.solution_tester.check_solution import get_test_results_from_solution

class CheckSolutionTest(unittest.TestCase):
    
    def test_get_test_results_from_solution(self):
        cwd = os.getcwd()
        os.chdir("../../island")
        
        print("CWD: " + cwd)
        print(os.listdir("."))
        
        
        
        testing_result = get_test_results_from_solution("island2_bv.cpp")
        
        print(testing_result.verdict+"!!!")
        
        os.chdir(cwd)
        
        #self.assertEqual(testing_result[""], second, msg)

if __name__ == "__main__":
    unittest.main()
