from logging import *
import time
from . import globalconfig
from .solution_tester import package_config
"""
   log-files : detailed.log   and  please.log
   logs added in matches.py only
"""

def update_shortname ():
    config = package_config.PackageConfig.get_config(".")
    if config:
        shortname = config['shortname']
    else:
        shortname = "Untitle"


logger = getLogger ("please_logger")
logger.setLevel(DEBUG)

sh = StreamHandler()
sh.setLevel(globalconfig.console_logging_lvl)

dfh = FileHandler('detailed.log')
dfh.setLevel(globalconfig.detailed_logging_lvl)

fh = FileHandler('please.log')
fh.setLevel(globalconfig.standart_logging_lvl)

shortname = "Untitle"
formatter = Formatter('%(asctime)s - ' + shortname + ' - %(name)s(%(levelname)s) %(message)s',datefmt='%d.%m.%Y[%H:%M:%S]')
console_formatter = Formatter(shortname + '(%(levelname)s) [%(asctime)s]: %(message)s',datefmt='%H:%M:%S')
fh.setFormatter(formatter)
sh.setFormatter(console_formatter)
dfh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(dfh)
logger.addHandler(sh)

config = package_config.PackageConfig.get_config(".")
if config:
    shortname = config['shortname']
else:
    shortname = "Untitle"
    
formatter = Formatter('%(asctime)s - ' + shortname + ' - %(name)s(%(levelname)s) %(message)s',datefmt='%d.%m.%Y[%H:%M:%S]')
console_formatter = Formatter(shortname + '(%(levelname)s) [%(asctime)s]: %(message)s',datefmt='%H:%M:%S')
fh.setFormatter(formatter)
sh.setFormatter(console_formatter)
dfh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(dfh)
logger.addHandler(sh)


logger.debug("The Please is running")
logger.debug("Logger was created")

if __name__ == "__main__":
    update_shortname()