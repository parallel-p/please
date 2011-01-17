#!/usr/bin/python

"""Localization utilities."""

_ru = {
    'log.debug': 'debug',
    'log.info': '',  # This is not shown anywhere, so it's empty.
    'log.notice': 'notice',
    'log.warning': 'warning',
    'log.error': 'error',
    'log.fatal': 'fatal',   
    
    'main.header': 'This is a please tool.',
    'main.unknown-context': 'Unknown environment. Use "please help".',
    'main.assuming-context': 'Assuming context: {0}.',
       
    'context.global.name': 'global',
    'context.problem.name': 'problem',

    'unknown-command-in-context': 'Unknown command "{command}" in {context} context. Use "please help [--all]".',
    'unknown-command': 'Unknown command "{0}". Use "please help --all".',
    'help.general-header': 'Usage: please <command> [options]\nVersion 0.1\nCommands are:',
    
    'commands.help.usage': 'usage: please help [command]',
    'commands.help.description': 'Print general or specific command help.',
    'commands.help.valid-options': 'Valid options are:',
    'commands.help.general-options': (
        'General options are:\n'
        '  --verbose\n'
        '    Show debug output.\n'
        '  --silent\n'
        '    Do not output anything.\n'),

    'options.parse-error': '{0}. Use: "please help {1}".',
    'options.usage-all': (
        '-a [--all]\n'
        '  Show help for all commands (not only specific to context).'),
    }

_current_locale = _ru

def get(name):
    return _current_locale[name]
