import unittest
import mox
from please.checker_runner import checker_runner
from please.solution_runner.solution_runner import run_solution, SolutionInfo
from please.invoker.invoker import ExecutionLimits, ResultInfo
import os
from please.solution_tester import tester
import sys

class SolutionTesterTest(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()
        
    def tearDown(self):
        self.mox.UnsetStubs()
        self.mox.VerifyAll()
        
    def a(self, a, b):
        return os.path.join(a, b)
    
    def q(self, verdict):
        return ResultInfo(verdict, 0, 0, 0, 0)

    #TODO: add tests with solution config

    def test_SimpleExpectedWA(self):
        config = {}
        config["solution_args"] = None
        config["checker"] = os.path.join("testdata", "checker.cpp")
        config["tests_dir"] = ".tests"
        config["expected"] = ["OK", "WA"]
        config["possible"] = ["TL"]
        config["execution_limits"] = None
        
        self.mox.StubOutWithMock(os.path, "exists")
        self.mox.StubOutWithMock(tester, "run_solution")
        self.mox.StubOutWithMock(checker_runner, "CheckerInfo")
        self.mox.StubOutWithMock(checker_runner, "run_checker")
        self.mox.StubOutWithMock(os, "remove")
        
        os.path.exists(os.path.join(".tests", "1")).AndReturn(True)
        info = ResultInfo("OK", 0, 0, 0, 0)
        
        tester.run_solution(mox.IgnoreArg()).AndReturn((info, "stdout", "stderr"))
        checker_runner.CheckerInfo(self.a('testdata','checker.cpp'), 
                                   self.a('.tests','1'),
                                   self.a('.tests','1.a'),
                                   self.a('.tests','.out')).AndReturn(None)
        infocheck = ResultInfo("OK", 0, 0, 0, 0)
        
        checker_runner.run_checker(None).AndReturn((infocheck, "stdout", "stderr"))
        os.path.exists(self.a(".tests", "2")).AndReturn(False)
        os.path.exists(self.a('.tests','.out')).AndReturn(True)
        os.remove(self.a('.tests','.out')).AndReturn(0)
        self.mox.ReplayAll()
        testing = tester.TestSolution(config)
        self.assertEqual(testing.test_solution(""), ({}, ["WA"], {self.a(".tests", "1"):\
                                                                  [self.q("OK"),"stdout","stderr"]}))
        
    def test_SimpleSuccessful(self):
        config = {}
        config["solution_config"] = None
        config["solution_args"] = None
        config["checker"] = os.path.join("testdata", "checker.cpp")
        config["tests_dir"] = ".tests"
        config["expected"] = ["OK"]
        config["possible"] = ["TL"]
        config["execution_limits"] = None
        
        self.mox.StubOutWithMock(os.path, "exists")
        self.mox.StubOutWithMock(tester, "run_solution")
        self.mox.StubOutWithMock(checker_runner, "CheckerInfo")
        self.mox.StubOutWithMock(checker_runner, "run_checker")
        self.mox.StubOutWithMock(os, "remove")
        
        os.path.exists(os.path.join(".tests", "1")).AndReturn(True)
        info = ResultInfo("OK", 0, 0, 0, 0)
        
        tester.run_solution(mox.IgnoreArg()).AndReturn((info, "stdout", "stderr"))
        checker_runner.CheckerInfo(self.a('testdata','checker.cpp'), 
                                   self.a('.tests','1'),
                                   self.a('.tests','1.a'),
                                   self.a('.tests','.out')).AndReturn(None)
        infocheck = ResultInfo("OK", 0, 0, 0, 0)
        
        checker_runner.run_checker(None).AndReturn((infocheck, "stdout", "stderr"))
        os.path.exists(self.a(".tests", "2")).AndReturn(False)
        os.path.exists(self.a('.tests','.out')).AndReturn(True)
        os.remove(self.a('.tests','.out')).AndReturn(0)
        self.mox.ReplayAll()
        testing = tester.TestSolution(config)
        self.assertEqual(testing.test_solution(""), ({}, [], {self.a(".tests", "1"):\
                                                              [self.q("OK"),"stdout","stderr"]}))
        
    def test_DifficultWithExpectedOK(self):
        config = {}
        config["solution_config"] = None
        config["solution_args"] = None
        config["checker"] = os.path.join("testdata", "checker.cpp")
        config["tests_dir"] = ".tests"
        config["expected"] = ["OK", "WA"]
        config["possible"] = ["TL"]
        config["execution_limits"] = None
        self.mox.StubOutWithMock(os.path, "exists")
        self.mox.StubOutWithMock(tester, "run_solution")
        self.mox.StubOutWithMock(checker_runner, "CheckerInfo")
        self.mox.StubOutWithMock(checker_runner, "run_checker")
        self.mox.StubOutWithMock(os, "remove")
        #
        os.path.exists(os.path.join(".tests", "1")).AndReturn(True)
        info = ResultInfo("OK", 0, 0, 0, 0)
        
        tester.run_solution(mox.IgnoreArg()).AndReturn((info, "stdout", "stderr"))
        checker_runner.CheckerInfo(self.a('testdata','checker.cpp'), 
                                   self.a('.tests','1'),
                                   self.a('.tests','1.a'),
                                   self.a('.tests','.out')).AndReturn(None)
        infocheck = ResultInfo("RE", 1, 0, 0, 0)
        
        checker_runner.run_checker(None).AndReturn((infocheck, "stdout", "stderr"))
        #
        os.path.exists(os.path.join(".tests", "2")).AndReturn(True)
        info = ResultInfo("TL", 0, 0, 0, 0)
        
        tester.run_solution(mox.IgnoreArg()).AndReturn((info, "stdout", "stderr"))
        #
        os.path.exists(self.a(".tests", "3")).AndReturn(False)
        os.path.exists(self.a('.tests','.out')).AndReturn(True)
        os.remove(self.a('.tests','.out')).AndReturn(0)
        self.mox.ReplayAll()
        testing = tester.TestSolution(config)
        self.assertEqual(testing.test_solution(""), ({}, ["OK"], 
                                                     {self.a(".tests", "1"):[self.q("WA"),"stdout","stderr"], 
                                                      self.a(".tests", "2"):[self.q("TL"),"",""]}))
        
    def test_SimpleUnexpectedWA(self):
        config = {}
        config["solution_config"] = None
        config["solution_args"] = None
        config["checker"] = os.path.join("testdata", "checker.cpp")
        config["tests_dir"] = ".tests"
        config["expected"] = []
        config["possible"] = ["TL"]
        config["execution_limits"] = None
        self.mox.StubOutWithMock(os.path, "exists")
        self.mox.StubOutWithMock(tester, "run_solution")
        self.mox.StubOutWithMock(checker_runner, "CheckerInfo")
        self.mox.StubOutWithMock(checker_runner, "run_checker")
        self.mox.StubOutWithMock(os, "remove")
        os.path.exists(os.path.join(".tests", "1")).AndReturn(True)
        info = ResultInfo("OK", 0, 0, 0, 0)
        
        tester.run_solution(mox.IgnoreArg()).AndReturn((info, "stdout", "stderr"))
        checker_runner.CheckerInfo(self.a('testdata','checker.cpp'), 
                                   self.a('.tests','1'),
                                   self.a('.tests','1.a'),
                                   self.a('.tests','.out')).AndReturn(None)
        infocheck = ResultInfo("RE", 1, 0, 0, 0)
        
        checker_runner.run_checker(None).AndReturn((infocheck, "stdout", "stderr"))
        os.path.exists(self.a(".tests", "2")).AndReturn(False)
        os.path.exists(self.a('.tests','.out')).AndReturn(True)
        os.remove(self.a('.tests','.out')).AndReturn(0)
        self.mox.ReplayAll()
        testing = tester.TestSolution(config)
        self.assertEqual(testing.test_solution(""),
                         ({"WA":[self.a(".tests","1")]}, [], {self.a(".tests","1"):\
                        [self.q("WA"), "stdout", "stderr"]}))
    
    def test_DifficultExpectedMLUnexpectedTLandOK(self):
        config = {}
        config["solution_config"] = None
        config["solution_args"] = None
        config["checker"] = os.path.join("testdata", "checker.cpp")
        config["tests_dir"] = ".tests"
        config["expected"] = ["ML"]
        config["possible"] = ["WA"]
        config["execution_limits"] = None
        self.mox.StubOutWithMock(os.path, "exists")
        self.mox.StubOutWithMock(tester, "run_solution")
        self.mox.StubOutWithMock(checker_runner, "CheckerInfo")
        self.mox.StubOutWithMock(checker_runner, "run_checker")
        self.mox.StubOutWithMock(os, "remove")
        #
        os.path.exists(os.path.join(".tests", "1")).AndReturn(True)
        info = ResultInfo("TL", 0, 0, 0, 0)
        
        tester.run_solution(mox.IgnoreArg()).AndReturn((info, "stdout", "stderr"))
        #
        os.path.exists(os.path.join(".tests", "2")).AndReturn(True)
        info = ResultInfo("OK", 0, 0, 0, 0)
        
        tester.run_solution(mox.IgnoreArg()).AndReturn((info, "stdout", "stderr"))
        checker_runner.CheckerInfo(self.a('testdata','checker.cpp'), 
                                   self.a('.tests','2'),
                                   self.a('.tests','2.a'),
                                   self.a('.tests','.out')).AndReturn(None)
        infocheck = ResultInfo("OK", 0, 0, 0, 0)
        
        checker_runner.run_checker(None).AndReturn((infocheck, "stdout", "stderr"))
        #
        os.path.exists(os.path.join(".tests", "3")).AndReturn(True)
        info = ResultInfo("OK", 0, 0, 0, 0)
        
        tester.run_solution(mox.IgnoreArg()).AndReturn((info, "stdout", "stderr"))
        checker_runner.CheckerInfo(self.a('testdata','checker.cpp'), 
                                   self.a('.tests','3'),
                                   self.a('.tests','3.a'),
                                   self.a('.tests','.out')).AndReturn(None)
        infocheck = ResultInfo("RE", 1, 0, 0, 0)
        
        checker_runner.run_checker(None).AndReturn((infocheck, "stdout", "stderr"))
        os.path.exists(self.a(".tests", "4")).AndReturn(False)
        os.path.exists(self.a('.tests','.out')).AndReturn(True)
        os.remove(self.a('.tests','.out')).AndReturn(0)
        self.mox.ReplayAll()
        testing = tester.TestSolution(config)
        self.assertEqual(testing.test_solution(""),
                         ({"TL":[self.a(".tests","1")],"OK":[self.a(".tests","2")]}, ["ML"],
                          {self.a(".tests","1"):[self.q("TL"),"",""],
                           self.a(".tests", "2"):[self.q("OK"),"stdout","stderr"],
                           self.a(".tests", "3"):[self.q("WA"),"stdout","stderr"]}))

if __name__ == '__main__':
    unittest.main()
