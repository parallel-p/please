import mox
import unittest
import please.checker_runner.checker_runner

class CheckerRunnerTest(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()
    
    def tearDown(self):
        self.mox.VerifyAll()
        self.mox.UnsetStubs()
    
    def test_checker_runner (self):
        self.mox.StubOutWithMock(please.executors.compiler, "compile")
        self.mox.StubOutWithMock(please.executors.runner, "run")
        please.executors.compiler.compile("test.cpp").AndReturn(1)
        please.executors.runner.run("test.cpp",["in.in", "out.out", "corr.corr"]).AndReturn(1)
        self.mox.ReplayAll()
        CInfo =  please.checker_runner.checker_runner.CheckerInfo("test.cpp", "in.in", "corr.corr", "out.out")
        result = please.checker_runner.checker_runner.run_checker(CInfo)
        self.assertEqual(result,1)
        
if __name__ == '__main__':
    unittest.main()      
