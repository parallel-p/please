from ..executors import compiler
from ..executors import runner
import shutil
import os

class CheckerCompileError(Exception):
    pass

class CheckerInfo:
    def __init__(self, source_path, input_file, correct_output, program_output):
        self.source_path = source_path
        self.args = [input_file, program_output, correct_output]

def run_checker (config):         
    result = compiler.compile(config.source_path)                        
    # info = result[0]
    # print("[debug] compile: ", result)
    # print("[debug]  verdict =", info.verdict)
    # print("[debug]  return_code =", info.return_code)
    # print("[debug]  real_time =", info.real_time)
    # print("[debug]  cpu_time =", info.cpu_time)
    # print("[debug]  used_memory =", info.used_memory)
    run_result = runner.run(config.source_path, config.args)
    return run_result


