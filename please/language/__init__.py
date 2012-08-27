from .language import Language

_lang = Language()

def get(path):
    '''Get a programming language for a file.'''
    return _lang.get(path)

def is_source_code(path):
    lang = get(path)
    return lang is not None and lang in langs # hey, there is TeX!

