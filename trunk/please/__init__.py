#!/usr/bin/python

"""Please is a command-line tool, which helps in developing and maintaining 
programming contests and problems."""

from . import contexts
from . import locale
from . import logging

import os.path
import sys

def Main(directory='.', args=None, log=None):
    """Main method to run please tool.
    
    Args:
        directory - root directory where to work from. Default is current dir.
        args - arguments (including command). Default are sys.argv.
        log - log instance. Default is console logger.
    """
    
    directory = os.path.abspath(directory)
    if args is None:
        args = sys.argv[1:]
    if log is None:
        log = logging.ConsoleLog()
    
    log.info(locale.get('main.header'))
    
    context = contexts.guess(directory, log)
    if context is None:
        log.error(locale.get('main.unknown-context'))
        return 1
        
    log.info(locale.get('main.assuming-context') % context.NAME)
    context.handle(args)
    return 0
