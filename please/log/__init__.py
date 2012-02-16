# coding: utf-8

from logging import Formatter as _Formatter, getLogger, DEBUG, StreamHandler, FileHandler
import os.path
from please import globalconfig
from colorama import init, Fore, Back, Style
from please.package import package_config
import inspect

"""
   log-files : detailed.log   and  please.log
   logs added in matches.py only
"""

init()
COLORS = {
    range(10, 20) : Fore.WHITE,                             # DEBUG
    range(20, 30) : Fore.WHITE + Style.BRIGHT,              # INFO
    range(30, 40) : Fore.YELLOW + Style.BRIGHT,             # WARNING
    range(40, 50) : Fore.RED + Style.BRIGHT,                # ERROR
    range(50, 99) : Fore.WHITE + Back.RED + Style.BRIGHT,   # CRITICAL
}
RESET = Fore.RESET + Back.RESET + Style.RESET_ALL

class Formatter(_Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%', colored=True):
        self.colored = colored
        return _Formatter.__init__(self, fmt, datefmt, style)

    def format(self, rec):
        if (self.colored):
            c = list(filter(lambda r: rec.levelno in r, list(COLORS)))
            color = COLORS[c[0]]
            return color + _Formatter.format(self, rec) + RESET
        else:
            return _Formatter.format(self, rec)

logger = getLogger ("please_logger")
logger.setLevel(DEBUG)

sh = StreamHandler()
sh.setLevel(globalconfig.console_logging_lvl)

dfh = FileHandler('detailed.log')
dfh.setLevel(globalconfig.detailed_logging_lvl)

fh = FileHandler('please.log')
fh.setLevel(globalconfig.standart_logging_lvl)

config = package_config.PackageConfig.get_config()

if config:
    shortname = config['shortname']
else:
    shortname = ""

file_fmt = Formatter('%(asctime)s - ' + shortname + ' - %(name)s(%(levelname)s) %(message)s',datefmt='%d.%m.%Y[%H:%M:%S]', colored=False)
console_fmt = Formatter(shortname + '(%(levelname)s) [%(asctime)s]: %(message)s',datefmt='%H:%M:%S', colored=True)
fh.setFormatter(file_fmt)
sh.setFormatter(console_fmt)
dfh.setFormatter(file_fmt)

logger.addHandler(fh)
logger.addHandler(dfh)
logger.addHandler(sh)

