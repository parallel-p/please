'''Language configuration automatics.'''

from .. import language
from importlib import import_module

modules = ["cpp",
           "dpr",
           "java",
           "command",
           "pdflatex",
           "python2",
           "python3",
           "perl",
          ]

configs = {}

for modname in modules:
    module = import_module('.' + modname, __name__)
    configs[module.LANGUAGE] = module.get_config()

def get_lang_config(source):
    lang = language.get(source)
    if lang in configs:
        return configs[lang](source)
    return None
