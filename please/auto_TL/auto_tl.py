import math
from .. import globalconfig
from ..solution_tester.package_config import PackageConfig
from ..solution_tester.check_solution import get_test_results_from_solution
from .. import svn
from ..utils.writepackage import writepackage

def set_integer_tl():
    opened_config = PackageConfig.get_config()
    solution = opened_config["main_solution"]
    opened_config["time_limit"] = globalconfig.default_limits.cpu_time
    result_dictionary = get_test_results_from_solution(solution, opened_config)[2]
    max_time = 0 
    for key, value in result_dictionary.items():
        max_time = max(max_time, value[0].cpu_time)
    seconds = math.ceil(max_time * 2)
    opened_config["time_limit"] = max(int(seconds), 1)
    writepackage(opened_config.get_text())
    
def set_float_tl():
    opened_config = PackageConfig.get_config()
    solution = opened_config["main_solution"]  
    opened_config["time_limit"] = globalconfig.default_limits.cpu_time
    result_dictionary = get_test_results_from_solution(solution, opened_config)[2]
    max_time = 0 
    for key, value in result_dictionary.items():
        max_time = max(max_time, value[0].cpu_time)
    seconds = max(0.1, math.ceil(max_time * 20) / 10)
    opened_config["time_limit"] = seconds
    writepackage(opened_config.get_text())
