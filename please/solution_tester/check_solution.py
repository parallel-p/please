import os.path
import logging
import colorama
from ..utils.platform_detector import get_platform
from ..solution_tester.package_config import PackageConfig
from ..invoker import invoker
from .. import globalconfig
from ..reports import generate_html_report
from ..utils.exception import Sorry

colorama.init()

logger = logging.getLogger("please_logger.check_solution")

class SolutionNotFoundException(Sorry):
    pass
        
def check_multiple_solution():
    """ Calls check_solution with different solution paths from config file including main solution """
    config = PackageConfig.get_config()
    # TODO: check if config is None
    generate_html_report.generate_html_report(config["solution"], True)
    
def check_main_solution():
    config = PackageConfig.get_config()
    # TODO: check if config is None
    # method check_solutions retrieves config from PackageConfig itself
    # remove it from here
    generate_html_report.generate_html_report([], True)
    
# Separate method for command line matcher
def check_solution(path):
    config = PackageConfig.get_config()
    # TODO: check if config is None
    # method check_solutions retrieves config from PackageConfig itself
    # remove it from here
    abspath = os.path.abspath(path)
    if abspath == os.path.abspath(config["main_solution"]):
        check_main_solution()
        return
    for solve in config["solution"]:
        if os.path.abspath(solve["source"]) == abspath:
            generate_html_report.generate_html_report([solve])
            return
    raise SolutionNotFoundException("There is no such solution")
    

