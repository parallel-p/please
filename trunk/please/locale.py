#!/usr/bin/python

"""Localization utilities."""

_ru = {
    'main.header': 'This is a please tool.',
    'main.unknown-context': 'Unknown environment. Use "please help".',
    'main.assuming-context': 'Assuming context: %s.',
       
    'context.global.name': 'global',
    'contexts.unknown-command-in-context': 'Unknown command "%(command)s" in %(context)s context. Use "please help".',
    
    'commands.help.name': 'help',
    'commands.update.name': 'update',
    }

_current_locale = _ru

def get(name):
    return _current_locale[name]
