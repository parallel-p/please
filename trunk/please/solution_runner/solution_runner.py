from ..executors import compiler
from ..executors.runner import run
import shutil
import os
import logging

log = logging.getLogger("please_logger.solution_runner.solution_runner")

class SolutionInfo:
    def __init__(self, source_path, args, execution_limits, solution_config,  solution_input_file, solution_output_file = None):
        #We dont need a config dictionary, we need to use a simple string with a path to the runnig test.
        self.source_path = source_path                   #Source path, string
        self.args = args                                 #Run arguments, list
        self.execution_limits = execution_limits         #Executon limits, class ExecutionLimits from Invoker
        self.solution_config = solution_config           #
        self.solution_input_file = solution_input_file   #Redirectering input file, string
        self.solution_output_file = solution_output_file #Rederectering output file, string  
        
def run_solution(config):
    """
    Description:
    Solution Runner compiles and runs solution
    
    sr = run_solution(solution_info)
    
    returns (invoker_result, stdout, stderr)
    invoker_result = ResultInfo
    
    """
    #config.config['input'] - solution input
    #solution_input_file - necessary file    

    while True:
        try:  # TODO: resolve this to something good in future
            stream_in = None
            stream_out = None

            solution_input = config.solution_config['input']
            solution_output = config.solution_config['output']

            if solution_input != 'stdin':
                shutil.copy(config.solution_input_file, solution_input)
            else:
                #TODO:make accurate closing of this file
                stream_in = open(config.solution_input_file, "r")
            if solution_output == 'stdout':
                stream_out = open(config.solution_output_file, 'w')
                
            compiler.compile(config.source_path)
            
            run_info, stdout, stderr = run(config.source_path, config.args, config.execution_limits, stream_in, stream_out)
            
            if stream_in:
                stream_in.close()
            if solution_input != 'stdin':
                os.remove(solution_input)
            
            if solution_output != 'stdout' and os.path.isfile(solution_output):
                shutil.move(solution_output, config.solution_output_file)
            
            if run_info.verdict == 'OK':
                with open(config.solution_output_file, 'r') as ouf:
                    stdout = ouf.read().encode()
            return (run_info, stdout, stderr)
        except OSError as e:
            if (e.errno == 13):
                log.warning('catched OSError 13/32, trying again...')
                continue
            raise e

