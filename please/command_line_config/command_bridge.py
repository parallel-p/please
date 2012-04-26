from please.command_line.template import Template
from please.commands import init_please_matcher
from please.log import logger

pm = init_please_matcher()

def call(args):
    res = pm.call(args)
    if not res:
        logger.error('unmatched command')

def add_simple_bridge(legacy_matcher):
    legacy_matcher.add_handler(
        Template(['_', '@args']),
                 call,
                 True)

