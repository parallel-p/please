from ..executors import compiler, runner
from ..invoker.invoker import ResultInfo
import logging    

from distutils.core import CompileError



def validate(validator, test):
        log = logging.getLogger("please_logger.validator_runner.validate")   
        try: 
                with open(test, 'rb') as f:    
                        try:
                                try:
                                        compiler.compile(validator)                                
                                        log.info("Validating %s by %s" % (test, validator))
                                        return runner.run(validator, stdin_fh=f)                                
                                except IOError:
                                        log.error("Validator " + validator + " not found")
                                        return (ResultInfo("FNF", 0, 0, 0, 1), "", "")
                        except compiler.CompileError as error:
                                log.error("Validator has an unknown extension, or does not compile with error: %s" % error)
                                return (ResultInfo("FNF", 0, 0, 0, 1), "", "")  

        except IOError:
                log.error("Test-File " + test + " not found")
                return (ResultInfo("FNF", 0, 0, 0, 1), "", "")
