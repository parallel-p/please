import unittest
import os.path
from please.solution_runner.solution_runner import SolutionInfo, run_solution
from please.invoker.invoker import ExecutionLimits

prefix = os.path.join('please', 'solution_runner', 'testdata')
class SolutionRunnerTest (unittest.TestCase) :
    
    def test_solution_runner_with_files(self) :
        info_class = SolutionInfo(os.path.join(prefix, "test.py"), 
                                  [], ExecutionLimits(), 
                                  {"input" : os.path.join(prefix, "result.in"), 
                                   "output" : os.path.join(prefix, "result.out")}, 
                                  os.path.join(prefix, "test.in"),
                                  os.path.join(prefix, "test.out" ))
        
        run_class = run_solution(info_class)

        output_file = open(os.path.join(prefix, "test.out"), "r")
        input_file = open(os.path.join(prefix, "test.in"), "r")
        self.assertEqual(input_file.read(), output_file.read())
        
    def test_solution_runner_with_stdstreams(self):
        info_class = SolutionInfo(os.path.join(prefix, "stdtest.py"), 
                                  [], ExecutionLimits(), 
                                  {"input" : "stdin", 
                                   "output" : "stdout"}, 
                                  os.path.join(prefix, "test.in"),
                                  os.path.join(prefix, "test.out" ))
        run_class = run_solution(info_class)
        output_file = open(os.path.join(prefix, "test.out"), "r")
        input_file = open(os.path.join(prefix, "test.in"), "r")
        self.assertEqual(input_file.read(), output_file.read())
if __name__ == '__main__':
    unittest.main()
	