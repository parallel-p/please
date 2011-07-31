import os
import shutil
import sys
import math
from ..package import config
from ..solution_tester.check_solution import get_test_results_from_solution
def __readpackage():
    input_stream = open("default.package", "r", encoding = "utf-8")
    config_file = input_stream.read()
    input_stream.close()
    return config_file
def __writepackage(text):
    output_stream = open("default.package", "w", encoding = "utf-8")
    output_stream.write(text)
    output_stream.close()
def set_integer_tl():
    config_text = __readpackage()
    opened_config = config.Config(config_text)
    solution = opened_config["main_solution"]
    opened_config["time_limit"] = 10
    result_dictionary = get_test_results_from_solution(solution,opened_config)
    max_time = 0 
    for key,value in result_dictionary.items():
        max_time = max(max_time,value[0].cpu_time)
    seconds = math.ceil(max_time*2)
    opened_config["time_limit"] = max(int(seconds),1)
    config_text = opened_config.get_text()
    __writepackage(config_text)
    
def set_float_tl():
    config_text = __readpackage()
    opened_config = config.Config(config_text)
    solution = opened_config["main_solution"]  
    opened_config["time_limit"] = 10
    result_dictionary = get_test_results_from_solution(solution,opened_config)
    max_time = 0 
    for key,value in result_dictionary.items():
        max_time = max(max_time,value[0].cpu_time)
    seconds = max(0.1,(math.ceil(max_time*20))/10)
    opened_config["time_limit"] = seconds
    config_text = opened_config.get_text()
    __writepackage(config_text)
