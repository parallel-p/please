from please.command_line.template import Template
from please.contest import commands as contest_commands


def add_contest_operations(matcher, active):
        matcher.add_handler(
                Template(["add", "problem|problems", "@problems", "to", "#name", "as", "@problems_as"]),
                contest_commands.command_add_problems,
                active)
        matcher.add_handler(
                Template(["add", "problem|problems", "@problems", "to", "#name"]),
                contest_commands.command_add_problems,
                active)
        matcher.add_handler(
                Template(["del|delete", "problem|problems", "@problems", "from", "#name"]),
                contest_commands.command_remove_problems,
                active)
        matcher.add_handler(Template(
                ["generate|gen", "contest", "#name", "statement|pdf"]),
                contest_commands.command_generate_statement,
                active)
        matcher.add_handler(
                Template(["export", "#name", "to", "#where", "as", "#contest"]),
                contest_commands.command_export,
                active)
        matcher.add_handler(Template(["change", "contest", "#name", "properties|prop", "#key", "#value"]),
                contest_commands.command_set_parameter,
                active)
