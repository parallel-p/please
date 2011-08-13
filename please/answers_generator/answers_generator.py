from ..solution_runner.solution_runner import SolutionInfo, run_solution
from please import globalconfig
import os
from ..package import config
from ..invoker.invoker import ExecutionLimits 
from ..solution_tester import package_config
from ..utils import utests
import logging
    
logger = logging.getLogger("please_logger.answers_generator")

class AnswersGenerator :
    """
     Description : 
      This class runs the solution (source_path) on list of tests (tests).
    
       tests - list of names of the tests
       source_path - path to the running solution
       solution_config = {"input" : solution_input_file, 
                 "output" : solution_output_file}
                 solution_input_file - the input file which is used in running solution
                 solution_input_file - the output file which is used in running solution 
       There are 2 methods :
         
         generate_without_arguments() - this method will parse problem config and geenrate all tests.
         generate(tests,source_path,args,execution_limits,solution_config) - this method is used by TestsAndAnswersGenerator
    """
    
    @staticmethod
    def generate_without_arguments () :
        """
        This is special method for generating tests using command : "please generate tests" 
        Your current location must be equal with the problems dir location.
        """
        #reading config
        opened_config = package_config.PackageConfig.get_config()    
        source_path = opened_config['main_solution']
        args = opened_config['args'] if 'args' in opened_config else []
        #float () - because opened_config['time_limit'] is str,
        #           but invoker uses float().
        execution_limits = ExecutionLimits(float(opened_config['time_limit']), float(opened_config['memory_limit']))
        solution_config = {"input" : opened_config['input'], "output" : opened_config['output']}
        #generating list of tests
        #running tests        
        for test in utests.get_tests(globalconfig.temp_tests_dir):
            run_solution (SolutionInfo (source_path, args, execution_limits, solution_config,
                                    os.path.join(globalconfig.temp_tests_dir, test), 
                                    os.path.join(globalconfig.temp_tests_dir, test + ".a")))
        
    
    def generate (self, tests, source_path, args, solution_config, execution_limits = globalconfig.default_limits) :
        for test in tests :
            logger.info('Generating answer for {0} with {1}'.format(str(test), str(source_path)))
            run_solution ((SolutionInfo (source_path, args, execution_limits,
                                         solution_config, test, test + ".a")))

    
