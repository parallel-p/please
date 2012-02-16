import os.path
from ..package.package_config import PackageConfig
from .. import globalconfig
from ..invoker import invoker


def make_config_with_solution_config(config, solution_config):
    # Get results from test_solution, create a config file to send.
    # Find all attributes from config's root or embedded solution's config        
    new_config = {}
    new_config["checker"] = config["checker"]
    new_config["tests_dir"] = globalconfig.temp_tests_dir #config["tests_dir"]        
    new_config["execution_limits"]  = invoker.ExecutionLimits(float(config["time_limit"]), float(config["memory_limit"]))
    new_config["solution_config"] = {"input":config["input"], "output":config["output"]}
    new_config["solution_args"] = [] #looks like solution needs no argument
    
    if solution_config is not None:
        new_config["expected"] = solution_config.get("expected") or globalconfig.default_expected
        new_config["possible"] = solution_config.get("possible") or globalconfig.default_possible
        if "OK" not in new_config["expected"] and "OK" not in new_config["possible"]:
            new_config["possible"] += ["OK"]
        if "input" in solution_config:
            new_config["solution_config"]["input"]  = solution_config["input"]
        if "output" in solution_config:
            new_config["solution_config"]["output"] = solution_config["output"]
    else:
        new_config["expected"] = globalconfig.default_expected
        new_config["possible"] = globalconfig.default_possible

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

