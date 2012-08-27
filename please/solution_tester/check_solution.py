import os.path
import logging
import colorama
from ..package.package_config import PackageConfig
from ..package.config import Config
from ..reports import generate_html_report
from ..utils.exceptions import PleaseException
from ..language.program_detector import is_program_detect

colorama.init()

logger = logging.getLogger("please_logger.check_solution")
        
def check_all_solutions():
    """ Calls check_solution with different solution paths from config file including main solution """
    config = PackageConfig.get_config()
    # TODO: check if config is None
    generate_html_report.generate_html_report(config["solution"]) #, True)
    
def check_main_solution():
    config = PackageConfig.get_config()
    # TODO: check if config is None
    # method check_solutions retrieves config from PackageConfig itself
    # remove it from here
    #generate_html_report.generate_html_report([]), True)
    check_solution(config.get_path('main_solution'))
    
def is_corresponded_solution(sol_path, substr):
    substr = os.path.normpath(substr)
    basename = os.path.basename(sol_path)
    #substring of basename or end of all path,
    #second condition allows to test solution by full path
    return substr == basename or sol_path.endswith(substr)

def is_standalone_solution(substr):
    return os.path.isfile(substr) and is_program_detect(substr) 

def check_solution(substr):
    config = PackageConfig.get_config()
    # TODO: check if config is None
    # method check_solutions retrieves config from PackageConfig itself
    # remove it from here

    solutions_for_testing = []
    #if full path specified for solution outside config
    if is_standalone_solution(substr):
        cfg = Config('')
        cfg.set_path("source", substr)
        fallback = [cfg]
    else:
        fallback = []
    for solve in config["solution"]:
        if is_corresponded_solution(solve["source"], substr):
            solutions_for_testing.append(solve)
    if len(solutions_for_testing) == 0:
        solutions_for_testing = fallback
    if len(solutions_for_testing) == 0:
        raise PleaseException("There is no such solution")
    generate_html_report.generate_html_report(solutions_for_testing) #, add_main)
    

