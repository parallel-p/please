from please.command_line.template import Template


def add_help_commands(matcher):
    from please.command_line.commands import print_help, print_lite_help
    matcher.add_handler(Template(["help"]), print_help, True)
    matcher.add_handler(Template(["commands"]), print_lite_help, True)


def add_todo_operations(matcher, active):
    from please.todo import todo_generator
    for tpl in [["show", "todo"], ["todo"]]:
        matcher.add_handler(Template(tpl),
                todo_generator.TodoGenerator.get_todo,
                active)
