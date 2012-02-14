import os.path
import logging
import colorama
from ..solution_tester.package_config import PackageConfig
from ..reports import generate_html_report
from ..utils.exceptions import PleaseException
from ..language import language

colorama.init()

logger = logging.getLogger("please_logger.check_solution")
        
def check_all_solutions():
    """ Calls check_solution with different solution paths from config file including main solution """
    config = PackageConfig.get_config()
    # TODO: check if config is None
    generate_html_report.generate_html_report(config["solution"], True)
    
def check_main_solution():
    #config = PackageConfig.get_config()
    # TODO: check if config is None
    # method check_solutions retrieves config from PackageConfig itself
    # remove it from here
    generate_html_report.generate_html_report([], True)
    
def is_cooresponded_solution(sol_path, substr):
    basename = os.path.basename(sol_path)
    #substring of basename or end of all path,
    #second condition allows to test solution by full path
    return substr in basename or sol_path.endswith(substr)

def is_standalone_solution(substr):
    return os.path.isfile(substr) and language.is_source_code(substr) 

def check_solution(substr):
    config = PackageConfig.get_config()
    # TODO: check if config is None
    # method check_solutions retrieves config from PackageConfig itself
    # remove it from here

    solutions_for_testing = []
    #if full path specified for solution outside config
    if is_standalone_solution(substr):
        solutions_for_testing.append({"source" : substr})
        add_main = False
    else:
        add_main = is_cooresponded_solution(config["main_solution"], substr)
        for solve in config["solution"]:
            if is_cooresponded_solution(solve["source"], substr):
                solutions_for_testing.append(solve)
        if not add_main and len(solutions_for_testing) == 0:
            raise PleaseException("There is no such solution")
    generate_html_report.generate_html_report(solutions_for_testing, add_main)
    

