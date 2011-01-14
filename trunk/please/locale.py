#!/usr/bin/python

"""Localization utilities."""

_ru = {
    'main.header': 'This is a please tool.',
    'main.unknown-context': 'Unknown environment. Use "please help".',
    'main.assuming-context': 'Assuming context: %s.',
       
    'context.global.name': 'global',
    'context.problem.name': 'problem',

    'unknown-command-in-context': 'Unknown command "%(command)s" in %(context)s context. Use "please help [--all]".',
    'unknown-command': 'Unknown command "%s". Use "please help --all".',
    'help.general-header': 'Usage: please <command> [options]\nVersion 0.1\nCommands are:',
    
    'commands.help.usage': 'usage: please help [command]',
    'commands.help.description': 'Print general or specific command help.',
    'commands.help.valid-options': 'Valid options are:',

    'options.use-help': 'Use: "please help %s".',
    'options.usage-all': ('-a [--all]\n'
                          '  Show help for all commands (not only specific to context).'),
    }

_current_locale = _ru

def get(name):
    return _current_locale[name]
