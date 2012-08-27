'''Matching sequence against many templates.'''

import logging
import textwrap

from . import template
from .template import Template

logger = logging.getLogger('please_logger.commands.Matcher')

PATH = object()
CUTOFF = 0.5
EPSILON = 0.1

class Matcher:
    def __init__(self):
        self.templates = []
        
    def add(self, template_string, handler, help = ''):
        '''Adds a template to a matcher.
        template_string is a string in format described in template.py.
        help is the help string for this template.'''
        self.templates.append((Template(template_string, help), handler))

    def match_template(self, seq):
        '''Match sequence against all templates until success,
        and returns appropriate template, handler and args,
        or None, None, None'''
        maxratio, maxhandler, maxdict = -1, None, None
        found = False
        for template, handler in self.templates:
            d, ratio = template.match_ratio(seq)
            if d is not None:
                if found:
                    if abs(maxratio - ratio) < EPSILON:
                        logger.warning('Command-line is ambiguous')
                else:
                    found = True
                if ratio > maxratio:
                    maxratio, maxtpl, maxhandler, maxdict = ratio, template, handler, d
        if maxratio >= CUTOFF:
            return maxtpl, maxhandler, maxdict

        return None, None, None

    def call(self, seq):
        '''Match against templates and call a handler.
        If match succeeded, return True. Else, return False.'''
        tpl, handler, args = self.match_template(seq)
        if handler is not None:
            handler(**args)
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
            if name[0].islower():
                f = getattr(m, name)
                if hasattr(f, '__call__'):
                    self.add_function(f)

    def get_completion(self, seq, start):
        '''Get a list of strings that can come after seq beginning with
        start; if path can come, then special value PATH will be present
        in the end of list.'''
        path = False
        answer = []
        for template, _ in self.templates:
            _, _, states = template.match_ratio_states(seq)
            for state in states:
                type, arg = template.tokens[state]
                if type == template.PATH:
                    path = True
                elif type == template.WORD:
                    # consider rewriting using generators and yield from
                    answer.extend(word for word in arg if word.startswith(start))
        if path:
            answer.append(PATH)
        return answer

