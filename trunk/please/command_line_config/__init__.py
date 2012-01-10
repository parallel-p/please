"""
Following function adds to matcher some commands
"""
from please.command_line.template import Template

from .formats import *
from .contest import *
from .help import *
from .solutions import *
from .package import *
from .execute import *
    
def add_creation_operations(matcher, active):
    from please.contest import commands as contest_commands
    from please.template import problem_template_generator
    matcher.add_handler(Template(["create", "problem", "#shortname"]),
            problem_template_generator.generate_problem, active)
    matcher.add_handler(Template(["create", "contest", "#name", "problems", "@problems"]),
            contest_commands.command_create_contest, active)

def add_aggregate_operations(matcher, active):
    from please.build_all.build_tools import build_all
    from please.cleaner import cleaner
    matcher.add_handler(
        Template(["clean|clear"]),
        cleaner.Cleaner().cleanup,
        active)
    for tpl in [["build", "all"], ["build"]]:
        matcher.add_handler(
            Template(tpl),
            build_all,
            active)



