from ..executors import compiler
from ..executors import runner

class CheckerInfo:
    def __init__(self, source_path, input_file, correct_output, program_output):
        self.source_path = source_path
        self.args = [input_file, program_output, correct_output]

def run_checker (config):
    result = compiler.compile(config.source_path)
    run_result = runner.run(config.source_path, config.args)
    return run_result


