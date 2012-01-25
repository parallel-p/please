from please.command_line.template import Template
from please.contest import commands as contest_commands
def add_contest_operations(matcher, active):
        matcher.add_handler(
                Template(["add", "@problems", "to", "#name", "@problems_as"]),
                contest_commands.command_add_problems,
                active)
        matcher.add_handler(
                Template(["add", "@problems", "to", "#name"]),
                contest_commands.command_add_problems,
                active)
        matcher.add_handler(
                Template(["remove|del", "@problems", "from", "#name"]),
                contest_commands.command_remove_problems,
                active)
        matcher.add_handler(Template(
                ["generate|gen", "statement|pdf", "for", "#name"]),
                contest_commands.command_generate_statement,
                active)
        matcher.add_handler(
                Template(["export", "#name", "to", "#where", "contest", "#contest"]),
                contest_commands.command_export,
                active)
        matcher.add_handler(Template(["set", "contest", "#name", "#key", "#value"]),
                contest_commands.command_set_parameter,
                active)


