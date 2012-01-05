import os.path
from ..solution_tester.package_config import PackageConfig
from .. import globalconfig
from ..invoker import invoker


def make_config_with_solution_config(config, solution_config):
    default_expected = ['OK']
    default_possible = []
    
    # Get results from test_solution, create a config file to send.
    # Find all attributes from config's root or embedded solution's config        
    new_config = {}
    new_config["checker"] = config["checker"]
    new_config["tests_dir"] = globalconfig.temp_tests_dir #config["tests_dir"]        
    new_config["execution_limits"]  = invoker.ExecutionLimits(float(config["time_limit"]), float(config["memory_limit"]))
    new_config["solution_config"] = {"input":config["input"], "output":config["output"]}
    new_config["solution_args"] = [] #looks like solution needs no argument
#    new_config["solution_args"] = config.get("solution_args") or []
    
    if solution_config is not None:
        #print("SOLUTION FOUND: " + sol_found["source"])               
        new_config["expected"] = solution_config.get("expected")
        new_config["possible"] = solution_config.get("possible")
        if "input" in solution_config:
            new_config["solution_config"]["input"]  = solution_config["input"]
        if "output" in solution_config:
            new_config["solution_config"]["output"] = solution_config["output"]
#        solution = os.path.abspath(sol_found["source"])
    else:
        pass
#        raise SolutionNotFoundException(solution + ' not found in config')

    new_config["expected"] = new_config.get("expected") or default_expected
    new_config["possible"] = new_config.get("possible") or default_possible
    return new_config
        
def make_config(solution, config = None):
    if config == None:
        config = PackageConfig.get_config()
        # TODO: check if config is sill None
        
    solution_config = None
    for cur_solution_config in config["solution"]:
        if cur_solution_config["source"] == os.path.relpath(solution):
#        if os.path.normpath(solution) in os.path.abspath(sol_found["source"]):
            solution_config = cur_solution_config
    
    return make_config_with_solution_config(config, solution_config)

