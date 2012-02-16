'''Matching sequence against many templates.'''

import logging
import textwrap

from .template import Template

logger = logging.getLogger('please_logger.commands.Matcher')

class Matcher:
    def __init__(self):
        self.templates = []
        
    def add(self, template_string, handler, help = ''):
        '''Adds a template to a matcher.
        template_string is a string in format described in template.py.
        help is the help string for this template.'''
        self.templates.append((Template(template_string, help), handler))

    def match(self, seq):
        '''Match sequence against all templates until success,
        and calls appropriate handler and returns True, if succeeded.
        Otherwise, returns False.'''
        maxratio, maxhandler, maxdict = -1, None, None
        found = False
        for template, handler in self.templates:
            d, ratio = template.match_ratio(seq)
            if d is not None:
                if found:
                    logger.warning('Command-line is ambiguous')
                if ratio > maxratio:
                    maxratio, maxhandler, maxdict = ratio, handler, d
        if maxratio >= 0:
            maxhandler(**maxdict)
            return True
        return False

    # User-friendly tools for adding functions.

    def add_function(self, f):
        '''Add a function to a default handler.
        First line of function docstring must contain a template,
        the rest being a documentation.'''
        doc = f.__doc__
        index = doc.find('\n')
        if index < 0:
            index = len(doc)

        template = doc[:index].strip()
        help = textwrap.dedent(doc[index + 1:])
        self.add(template, f, help)

    def add_module(self, m):
        '''Adds every function in module if function name starts with 'handle'.'''
        for name in dir(m):
            if name.startswith('handle_'):
                f = getattr(m, name)
                if hasattr(f, '__call__'):
                    self.add_function(f)

