from please.command_line.template import Template


def add_solution_modifications(matcher, active):
        from please.add_source.add_source import del_props, del_solution,\
                                                 add_solution, add_main_solution,\
                                                 change_solution
        matcher.add_handler(Template(["set", "main", "solution", "$path"]), add_main_solution, active)
        matcher.add_handler(
                Template(["add", "solution|sol", "$path"]),
                add_solution, active)
        matcher.add_handler(
                Template(["add", "solution|sol", "$path", "@args"]),
                add_solution, active)
        matcher.add_handler(
                Template(["delete|del", "solution|sol", "#path"]),
                del_solution, active)
        matcher.add_handler(
                Template(["change", "prop|properties", "@args"]),
                change_solution, active)
        matcher.add_handler(
                Template(["delete|del", "prop|properties", "@args"]),
                del_props, active)


def add_checking_solution_operations(matcher, active):
    from please.solution_tester import check_solution
    for tpl in [["run|check", "solutions|sols|all"], "check|run all solutions|sols".split()]:
        matcher.add_handler(
                Template(tpl),
                check_solution.check_all_solutions,
                active)

    #TODO:support checking several but not all solutions

    #TODO:support "check #path" in current implementation it is
    #conflict with "check main|all|sols|solutions"
    for tpl in [["check|run", "solution|sol|solutions|sols", "#substr"]]:
        matcher.add_handler(
            Template(tpl),
            check_solution.check_solution,
            active)

    for tpl in [["check|run", "main", "solution|sol"], ["check", "main"]]:
        matcher.add_handler(
            Template(tpl),
            check_solution.check_main_solution,
            active)


