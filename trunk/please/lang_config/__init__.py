'''Language configuration automatics.'''

from importlib import import_module
from .detection import LanguageDetector

_detector = LanguageDetector()

_configs = {}

modules = ["cpp",
           "dpr",
           "java",
           "command",
           "pascal",
           "pdflatex",
           "python",
           "perl",
           "perl",
          ]

for modname in modules:
    module = import_module('.' + modname, __name__)
    _detector._add_module(module)
    _configs[module.LANGUAGE] = module.get_config()

def get_language(path):
    return _detector.get_name(path)

def get_lang_config(source):
    lang = get_language(source)
    if lang in _configs:
        return _configs[lang](source)
    return None
