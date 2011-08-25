#!/usr/bin/python3
from please import log
import logging
from .command_line.matcher import Matcher
from .command_line.template import Template
from .latex import latex_tools
from .template import problem_template_generator as problem_gen
from .package import config
import codecs
import sys
from . import globalconfig
from .solution_tester.package_config import PackageConfig

def __writepackage(text):
    output_stream = open(globalconfig.default_package, "w", encoding = "utf-8")
    output_stream.write(text)
    output_stream.close()

def add_tags (tags):
    opened_config = PackageConfig.get_config()
    
    if not "tags" in opened_config:
        opened_config["tags"] = ""
    
    s = "; ".join(tags)
    
    if (opened_config["tags"] != ''):
        s = opened_config["tags"] + "; " + s

    opened_config["tags"] = s
    config_file = opened_config.get_text()
    __writepackage(config_file)
    
def clear_tags ():
    opened_config = PackageConfig.get_config()
    if not "tags" in opened_config:
        pass
    opened_config["tags"] = " "
    config_file = opened_config.get_text()
    __writepackage(config_file)   
    
def show_tags ():
    _inst_logger= logging.getLogger ("please_logger.tags.show_tags")
    _inst_logger.debug("Output Tags")
    opened_config = PackageConfig.get_config()
    if "tags" in opened_config:
        print(opened_config["tags"])   

def set_name(name):
    opened_config = PackageConfig.get_config()
    opened_config["name"] = name
    __writepackage(opened_config.get_text())