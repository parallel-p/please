from ..executors import compiler
from ..executors.runner import run
import sys
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
            if config.solution_config['input'] != 'stdin':
                shutil.copy(config.solution_input_file, config.solution_config['input'])
            else:
                #TODO:make accurate closing of this file
                stream_in = open(config.solution_input_file, "r")
            if config.solution_config['output'] == 'stdout':
                stream_out = open(config.solution_output_file, 'w')
                
            compiler.compile(config.source_path)
            
            run_dump = run(config.source_path, config.args, config.execution_limits, stream_in, stream_out)
            # info = run_dump[0]
            # print("[debug] run_dump =", run_dump)
            # print("[debug]  verdict =", info.verdict)
            # print("[debug]  return_code =", info.return_code)
            # print("[debug]  real_time =", info.real_time)
            # print("[debug]  cpu_time =", info.cpu_time)
            # print("[debug]  used_memory =", info.used_memory)
        
            if stream_in:
                stream_in.close()
            if config.solution_config['input'] != 'stdin':
                os.remove(config.solution_config['input'])
            
            if config.solution_config['output'] != 'stdout':
                try:
                    shutil.copy(config.solution_config['output'], config.solution_output_file)
                    os.remove(config.solution_config['output'])
                except:
                    pass
            else:
                pass
        
            if run_dump[0].verdict == 'OK':
                with open(config.solution_output_file, 'r') as ouf:
                    run_dump = (run_dump[0], ouf.read().encode(), run_dump[2])
            return run_dump
        except OSError as e:
            if (e.errno == 13):
                log.info('catched OSError 13/32, trying again...')
                continue
            raise e

