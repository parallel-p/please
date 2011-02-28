#!/usr/bin/python

"""Localization utilities."""

from . import config

_en = {
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


    'user-input-error': '{0}. Use: "please help {1}".',
    'user-input-error-no-command': '{0}.',
    'unknown-command-in-context': 'Unknown command "{command}" in {context} context. Use "please help [--all]"',
    'unknown-command': 'Unknown command "{0}". Use "please help --all"',
    'too-much-arguments': 'Too much arguments',
    'not-enough-arguments': 'Not enough arguments',
    'general-error': 'An error occured: {0}', 
    'malformed-problem-error': 'Malformed problem: {0}',
    
    'done': 'Done!',


    'problem.checker-not-found': 'checker is not found',
    'problem.validator-not-found': 'validator is not found',
    'problem.validator-found': 'validator = %s',
    'problem.checker-found': 'checker = %s',
    'problem.generate-not-found': "please generate file not found at '%s'" % config.config.generateFile(),
    'problem.statements-found': 'statements = %s',
    'problem.statements-not-found': "statements not found",

    
    'commands.help.usage': 'usage: please help [command] [options]',
    'commands.help.description': 'Print general or specific command help.',
    'commands.help.valid-options': 'Valid options are:',
    'commands.help.general-header': 'Usage: please <command> [options]\nVersion 0.1\nCommands are:',
    'commands.help.general-options': (
        'General options are:\n'
        '  --verbose\n'
        '    Show debug output.\n'
        '  --silent\n'
        '    Do not output anything.\n'),
    
    'commands.run.description': 'Runs selected executable (or script) with time and memory limits.',
    'commands.run.usage': 'usage: please run FILE [options]',

    'commands.inspect.usage': 'usage: please inspect',
    'commands.inspect.description': 'Check whether problem is well-formed.',
    'commands.inspect.header': 'Inspecting problem "{0}".',

    'commands.statement.usage': 'usage: please statement',
    'commands.statement.description': 'Compile statement into pdf.',
    'commands.statement.header': 'Compiling statement for problem "{0}"...',
    'commands.statement.preparing-tex-file': 'Preparing TeX file with statements...',
    'commands.statement.running-tex': 'Running TeX...',
    'commands.statement.moving-pdf': 'Moving .ps and .pdf files...',
    
    'commands.generate.usage': 'usage: please generate', 
    'commands.generate.description': 'Generates tests', 
    'commands.generate.header': 'Generating tests for problem "{0}"', 
    'commands.generate.running-script': 'Running generator script "{0}"', 

    'generator.running-command': 'Running command "{0}"', 
    'generator.test-found': 'Found tests %d in file "%s", to be renamed to "%s"', 
    'generator.answer-found': '   ... and answer in file "%s", to be renamed to "%s"', 

    'options.usage-all': (
        '-a [--all]\n'
        '  Show help for all commands (not only specific to context).'),
    }

_current_locale = _en

def get(name):
    return _current_locale[name]
