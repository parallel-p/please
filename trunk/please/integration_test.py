import sys
import os
import shutil
import unittest
from please import log

from please import launcher
try:
    from unittest.mock import call, Mock
except ImportError:
    from mock import call, Mock

start_dir = os.getcwd()
script_dir = os.path.dirname(__file__)
testdata_dir = os.path.join(os.path.dirname(__file__), 'testdata')
problem1_dir = os.path.join(testdata_dir, 'problem1')


class CommandsTest(unittest.TestCase):

    def setUp(self):
        log.logger.debug = Mock()
        log.logger.info = Mock()
        log.logger.error = Mock()
        log.logger.warning = Mock()
        log.logger.critical = Mock()

    def tearDown(self):
        pass

    def test_please_blablabla(self):
        sys.argv = ['please', 'blablabla']
        launcher.main()
        self.assertEqual([call('Please error: No functions match the template entered')], log.logger.error.call_args_list)

    def test_please_noargs(self):
        sys.argv = ['please']
        launcher.main()
        self.assertEqual(log.logger.info.call_args_list, [call("Type 'please commands' to show all available commands or 'please help' to show them with detailed description")])

    def test_please_help(self):
        sys.argv = ['please', 'help']
        launcher.main()
        self.assertEqual(log.logger.error.call_args_list, [])

    def test_please_commands(self):
        sys.argv = ['please', 'commands']
        launcher.main()
        self.assertEqual(log.logger.error.call_args_list, [])

class CommandsTestWithCreateProblem(unittest.TestCase):

    def setUp(self):
        log.logger.debug = Mock()
        log.logger.info = Mock()
        log.logger.error = Mock()
        log.logger.warning = Mock()
        log.logger.critical = Mock()
        os.chdir(testdata_dir)

    def tearDown(self):
        shutil.rmtree('testproblem')
        os.chdir(start_dir)


class CommandsTestWithContest(unittest.TestCase):

    def setUp(self):
        log.logger.debug = Mock()
        log.logger.info = Mock()
        log.logger.error = Mock()
        log.logger.warning = Mock()
        log.logger.critical = Mock()
        os.chdir(testdata_dir)

    def tearDown(self):
        os.remove('test.contest')
        os.chdir(start_dir)

    def test_create_contest(self):
        sys.argv = ['please', 'create', 'contest', 'test', 'of', 'problem1', 'problem2']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_add_delete_from_contest(self):
        sys.argv = ['please', 'create', 'contest', 'test', 'of', 'problem1', 'problem2']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'delete', 'problem', 'problem2', 'from', 'test']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'add', 'problem', 'problem2', 'to', 'test']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'del', 'problem', 'problem1', 'from', 'test']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'add', 'problems', 'problem1', 'to', 'test']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_gen_contest_statements(self):
        sys.argv = ['please', 'create', 'contest', 'test', 'of', 'problem1', 'problem2']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'gen', 'contest', 'test', 'statements']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'generate', 'contest', 'test', 'pdf']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        shutil.rmtree('.statements')
        os.remove('test.pdf')

    def test_change_prop_contest(self):
        sys.argv = ['please', 'create', 'contest', 'test', 'of', 'problem1', 'problem2']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)
        sys.argv = ['please', 'change', 'contest', 'test', 'prop', 'name', 'AAA']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)


class CommandsTestInsideProblem1(unittest.TestCase):

    def setUp(self):
        log.logger.debug = Mock()
        log.logger.info = Mock()
        log.logger.error = Mock()
        log.logger.warning = Mock()
        log.logger.critical = Mock()
        os.chdir(problem1_dir)

    def tearDown(self):
        os.chdir(start_dir)

    def test_build_all(self):
        sys.argv = ['please', 'build', 'all']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_build(self):
        sys.argv = ['please', 'build']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_clean(self):
        sys.argv = ['please', 'build']
        launcher.main()
        sys.argv = ['please', 'clean']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_generate_tests(self):
        sys.argv = ['please', 'generate', 'tests']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_generate_tests_with_tags(self):
        sys.argv = ['please', 'generate', 'tests', 'with', 'tag', 'sample']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_gen_tests(self):
        sys.argv = ['please', 'gen', 'tests']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_generate_answers(self):
        sys.argv = ['please', 'generate', 'answers']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_gen_ans(self):
        sys.argv = ['please', 'generate', 'answers']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_generate_statements(self):
        sys.argv = ['please', 'generate', 'statements']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_gen_pdf(self):
        sys.argv = ['please', 'gen', 'pdf']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_todo(self):
        sys.argv = ['please', 'todo']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_val_tests(self):
        sys.argv = ['please', 'val', 'tests']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_validate_tests(self):
        sys.argv = ['please', 'validate', 'tests']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_validate(self):
        sys.argv = ['please', 'validate']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_set_validator(self):
        sys.argv = ['please', 'set', 'validator', 'val.cpp']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'set', 'val', 'val.cpp']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_stress_with_args(self):
        sys.argv = ['please', 'stress',  'solutions/wrong.dpr', 'gen.dpr', 'with', 'args', '100']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 1)

    def test_stress(self):
        sys.argv = ['please', 'stress',  'solutions/wrong.dpr', 'gen2.dpr']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 1)

    def test_stress_correct(self):
        sys.argv = ['please', 'stress',  'solutions/prev_ni.py', 'solutions/wrong.dpr', 'gen2.dpr']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 1)

    def test_stress_correct_with_args(self):
        sys.argv = ['please', 'stress',  'solutions/prev_ni.py', 'solutions/wrong.dpr', 'gen2.dpr', 'with', 'args', '100']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 1)

    def test_tags(self):
        sys.argv = ['please', 'tags']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_show_tags(self):
        sys.argv = ['please', 'show', 'tags']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_clear_tags(self):
        sys.argv = ['please', 'clear', 'tags']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_add_tags(self):
        sys.argv = ['please', 'add', 'tags', 'tag1', 'tag2', 'tag3']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_compute_tl(self):
        sys.argv = ['please', 'compute', 'tl']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_compute_integer_timelimit(self):
        sys.argv = ['please', 'compute', 'integer', 'timelimit']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_set_standart_checker(self):
        sys.argv = ['please', 'set', 'standart', 'checker']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_set_std_checker(self):
        sys.argv = ['please', 'set', 'stdt', 'checker']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_set_checker_name(self):
        sys.argv = ['please', 'set', 'standart', 'checker', 'icmp']
        launcher.main()
        sys.argv = ['please', 'set', 'checker', 'check.cpp']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_set_std_checker_name(self):
        sys.argv = ['please', 'set', 'std', 'checker', 'fcmp']
        launcher.main()
        sys.argv = ['please', 'set', 'checker', 'check.cpp']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_problem_config_set(self):
        sys.argv = ['please', 'set', 'name', 'aaa']
        launcher.main()
        sys.argv = ['please', 'set', 'problem', 'name', 'b24']
        launcher.main()
        sys.argv = ['please', 'set', 'input', 'stdin']
        launcher.main()
        sys.argv = ['please', 'set', 'input', 'prev.in']
        launcher.main()
        sys.argv = ['please', 'set', 'output', 'stdout']
        launcher.main()
        sys.argv = ['please', 'set', 'output', 'prev.out']
        launcher.main()
        sys.argv = ['please', 'set', 'time_limit', '2.1']
        launcher.main()
        sys.argv = ['please', 'set', 'ML', '128']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_zip(self):
        sys.argv = ['please', 'zip']
        launcher.main()
        os.remove('package.zip')
        self.assertEqual(log.logger.error.call_count, 0)

    def test_solutions(self):
        sys.argv = ['please', 'check', 'solution']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'run', 'sols']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'check', 'all']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'run', 'all', 'sols']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'check', 'all', 'solutions']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'check', 'sol', 'prev_ni.py']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'check', 'sol', 'ni']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'run', 'solution', 'solutions/prev_st.dpr']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'check', 'main', 'solution']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'run', 'main', 'sol']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'check', 'main']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_set_main_solution(self):
        sys.argv = ['please', 'set', 'main', 'solution', 'solutions/prev_ni.py']
        launcher.main()
        sys.argv = ['please', 'set', 'main', 'solution', 'solutions/prev_st.dpr']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_add_delete_solution(self):
        sys.argv = ['please', 'add', 'solution', 'solutions/wrong.dpr']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        sys.argv = ['please', 'delete', 'solution', 'solutions/wrong.dpr']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

    def test_add_delete_solution_verdicts(self):
        sys.argv = ['please', 'add', 'solution', 'solutions/wrong.dpr', 'expected', 'WA', 'TL', 'possible', 'OK']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        self.assertEqual(log.logger.error.call_count, 0)
        sys.argv = ['please', 'change', 'prop', 'solutions/wrong.dpr', 'expected', 'WA', 'OK', 'possible', 'TL']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        self.assertEqual(log.logger.error.call_count, 0)
        sys.argv = ['please', 'del', 'prop', 'solutions/wrong.dpr', 'expected']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

        self.assertEqual(log.logger.error.call_count, 0)
        sys.argv = ['please', 'delete', 'solution', 'solutions/wrong.dpr']
        launcher.main()
        self.assertEqual(log.logger.error.call_count, 0)

if __name__ == '__main__':
    unittest.main()
