from ..executors import compiler, runner
from ..invoker.invoker import ResultInfo
import logging

def validate(validator, test):
        log = logging.getLogger("please_logger.validator_runner.validate")
        with open(test, 'rb') as f:    
                compiler.compile(validator)                         
                return runner.run(validator, stdin_fh=f)
