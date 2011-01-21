import unittest
from mock import Mock
from problem import Problem

class ProblemTest(unittest.TestCase):

    def file_system_mock(self, cfg_context):
        read_mock = Mock(return_value = cfg_context)
        exists_mock = Mock(return_value = True)
        fs = Mock()
        fs.read = read_mock
        fs.exists = exists_mock
        return fs


    def test_simple_parsing(self):

        cfg_context = "\n".join(["please_version=0.1", "tags=naive",
             "input=aplusb.in", "output=aplusb.out",
             "check=check.cpp", "validator=val.pas"])
        problem = Problem(self.file_system_mock(cfg_context))
        self.assertEqual(problem.input(), "aplusb.in")
        self.assertEqual(problem.output(), "aplusb.out")

        validator = problem.validator()
        #TODO: mock this class. just check constructor called
        self.assertEqual(validator.file(), "val.pas")
        self.assertEqual(validator.input(), "stdin")
        self.assertEqual(validator.output(), "stdout")

        checker = problem.checker()
        #TODO: mock this class. just check constructor called
        self.assertEqual(checker.file(), "check.cpp")

        statements = problem.statements()
        #TODO: mock this class. just check constructor called
        self.assertEqual(statements, None)

if __name__ == '__main__':
    unittest.main()
