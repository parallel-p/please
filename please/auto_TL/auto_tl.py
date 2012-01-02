import math
from .. import globalconfig
from ..solution_tester.package_config import PackageConfig
from ..solution_tester.check_solution import get_test_results_from_solution
from .. import svn
from ..utils.writepackage import writepackage
import logging

logger = logging.getLogger("please_logger.auto_TL.auto_tl")

def compute_exec_times():
    logger.warning("Remember: TL is setting by execution results of main solution, so it should be the slowest solution")
    opened_config = PackageConfig.get_config()
    solution = opened_config["main_solution"]
    opened_config["time_limit"] = globalconfig.default_limits.cpu_time
    result_dictionary = get_test_results_from_solution(solution, opened_config)[2]
    max_time = 0 
    for key, value in result_dictionary.items():
        max_time = max(max_time, value[0].cpu_time)
    return max_time, opened_config
        
def set_in_package(time, config):
    config["time_limit"] = time
    writepackage(config.get_text())
    
def set_integer_tl():
    max_time, config = compute_exec_times()
    seconds = max(int(math.ceil(max_time * 2)), 1)
    set_in_package(seconds, config)
    logger.warning("Maximal execution time: " + str(max_time) + ", now TL in default.package is: " + str(seconds))
    
def set_float_tl():
    max_time, config = compute_exec_times()
    seconds = max(0.1, math.ceil(max_time * 20) / 10)
    set_in_package(seconds, config)
    logger.warning("Maximal execution time: " + str(max_time) + ", now TL in default.package is: " + str(seconds))
    
