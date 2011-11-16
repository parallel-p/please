from ..checker_runner import checker_runner
from ..solution_runner.solution_runner import run_solution, SolutionInfo
from ..invoker.invoker import ExecutionLimits
from .. import globalconfig
from ..utils import utests
from ..utils.error_window import PreventErrorWindow
from ..utils import form_error_output
import os
import logging

logger = logging.getLogger("please_logger.solution_tester.tester")

class TestSolution:
    '''Tests given solution.
        Usage:
            config = {}
            config["checker"] = "checker.cpp"
            config["tests_dir"] = ".tests"
            config["expected_verdicts"] = ["OK", "ML"]
            config["optional_verdicts"] = ["TL"]
            config["execution_limits"] = ExecutionLimits()
            config["solution_config"] = ... (nobody knows now :-))
            config["solution_args"] = ["-p", "-f"]
            tester = TestSolution(config)
            result = tester.test_solution("solution.dpr")
         Returns:
            result is tuple of:
                a) dictionary of unexpected, but met verdicts and list of paths to
                tests, where it happened
                b) list of expected, but not met verdicts
                c) and dictionary of tests names and list of
                    1) checker verdict on them
                    2) and real time of solution running
            Sample:
                result = ( {"WA":[".tests/1", ".tests/2"], "PE":[".tests/17"]}, ["OK", "ML"],
                {".tests/1":[ResultInfo, stdout, stderr], 
                ".tests/2":[ResultInfo, stdout, stderr], ... , 
                ".tests/17":[ResultInfo, stdout, stderr], 
                ".tests/18":[ResultInfo, stdout, stderr]})
     '''
    def __init__(self, config):
        #all necessary parameters in config are below:
        self.checker = config["checker"]
        self.tests_dir = config["tests_dir"]
        if "expected_verdicts" in config:
            self.expected_verdicts = config["expected_verdicts"] 
        else:
            self.expected_verdicts = [] 
        self.optional_verdicts = config["optional_verdicts"] or []
        self.execution_limits = config["execution_limits"] or globalconfig.default_limits
        self.solution_config = config["solution_config"]
        self.solution_args = config["solution_args"]
        
    def one_test(self, solution, test, answer, program_out):
        logger.info('Testing {0} on {1}'.format(solution, test))
        with PreventErrorWindow():
#        error_window(hide = True)
            solution_info = SolutionInfo(solution, self.solution_args, self.execution_limits, \
                                                             self.solution_config, test, program_out)
            solution_run_result = run_solution(solution_info)
            result = ""
            stdout = ""
            stderr = ""
            if solution_run_result[0].verdict != "OK":
                if solution_run_result[0].verdict == "RE":
                    logger.error("Solution has had RE with exit code: " + str(solution_run_result[0].return_code))
                    out_err = form_error_output.form_err_string_by_std(solution_run_result[1], solution_run_result[2].decode())
                    if out_err != "":
                        logger.error(out_err)
                result = solution_run_result[0].verdict
            else:
                checker_info = checker_runner.CheckerInfo(self.checker, test, answer, program_out)
                check_result = checker_runner.run_checker(checker_info) 
                #tuple: ResultInfo, stdout, stderr
                if check_result[0].return_code in globalconfig.checker_return_codes:
                    result = globalconfig.checker_return_codes[check_result[0].return_code]
                else:
                    result = "CF"
                stdout = check_result[1]
                stderr = check_result[2]
            #take return code + realtime
            result_info = solution_run_result[0]
            result_info.verdict = result
#        error_window(hide = False)
        return [result_info, stdout, stderr]
        
    def test_solution(self, solution):  
        met_not_expected = {}
        expected_not_met = []
        testing_result = {}
        verdicts = dict(zip(self.expected_verdicts, [0] * len(self.expected_verdicts))) 
        #{"WA":0, "OK":0, "TL":0 ... }
        program_out = os.path.join(self.tests_dir, globalconfig.temp_solution_out_file)
        #.tests/out
        for test in utests.get_tests(self.tests_dir):
            #.tests/1, .tests/2 ...
            answer = test + ".a" 
            #.tests/1.a, .tests/2.a ...
            result = self.one_test(solution, test, answer, program_out)
            if result[0].verdict in verdicts:
                verdicts[result[0].verdict] += 1
            elif result[0].verdict not in self.optional_verdicts:
                met_not_expected.setdefault(result[0].verdict, []).append(test) 
                #{"PE":[".tests/1", ".tests/4"]}
            testing_result[test] = result
            #{".tests/1":[ResultInfo,stdout,stderr], ".tests/2":[ResultInfo,stdout,stderr]}
        for item, value in verdicts.items():
            if value == 0: #if didn't meet
                expected_not_met.append(item) #["WA", "TL"]
        if os.path.exists(program_out):
            os.remove(program_out)
        return (met_not_expected, expected_not_met, testing_result)
            
