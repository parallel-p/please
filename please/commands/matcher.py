'''Matching sequence against many templates.'''

from .template import Template

class Matcher:
    def __init__(self):
        self.templates = []
        
    def add(self, template_string, handler):
        '''Adds a template to a matcher.
        template_string is a string in format described in template.py.'''
        self.templates.append((Template(template_string), handler, assertion))

    def match(self, seq):
        '''Match sequence against all templates until success,
        and calls appropriate handler and returns True, if succeeded.
        Otherwise, returns False.'''
        for template, handler in self.templates:
            d = template.match(seq)
            if d is not None:
                handler(**d)
                return True
        return False

    # User-friendly tools for adding functions.

    def add_function(self, f):
        '''Add a function to a default handler.
        First line of function docstring must contain a template,
        the rest being a documentation.'''
        doc = f.__doc__
        template = doc.split('\n', 1)[0]
        self.add(template, f)

    def add_module(self, m):
        '''Adds every function in module if function name starts with 'handle'.'''
        for name in dir(m):
            if name.startswith('handle_'):
                f = getattr(m, name)
                if hasattr(f, '__call__'):
                    self.add_function(f)

