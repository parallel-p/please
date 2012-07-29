import os

def help(command = None):
    '''help [command...]
    Help on a command or write a list of commands.'''
    from please.commands import get_matcher
    m = get_matcher('please')
    if command is None or command == ['commands']:
        for template, func in m.templates:
            h = template.format()
            if h:
                print(h)
                print()
    elif command == ['me', 'Eirin']:
        print('Nice try, but I do not know path to Gensokyo.')
        print('Neither Eirin am I.')
    else:
        tpl = m.match_template(command)[0]
        if tpl is None or tpl.help() is None:
            print("I don't know how to " + ' '.join(command))

def determine_location():
    """
        Returns True is location is root of the problem
    """
    from please import globalconfig
    from please.package import package_config
    startdir = current_dir = os.getcwd()
    prev_dir = None
    pkg = package_config.PackageConfig.get_config()
    while current_dir != prev_dir and pkg is None:
        prev_dir = current_dir
        os.chdir('..')
        current_dir = os.getcwd()
        pkg = package_config.PackageConfig.get_config()
    if pkg is None:
        os.chdir(startdir)
    in_problem_folder = (pkg is not None)
    globalconfig.in_problem_folder = in_problem_folder
    return in_problem_folder, startdir

def legacy(command):
    '''legacy command...
    Execute command using legacy matcher.'''
    from please.command_line.matcher import Matcher
    from please.log import logger
    from please.utils.exceptions import PleaseException, MatcherException
    from please import command_line_config
    
    in_problem_folder, startdir = determine_location()
    matcher = Matcher()
    matcher.startdir = startdir
    command_line_config.add_help_commands(matcher)

    command_line_config.add_creation_operations(matcher,
        active=not in_problem_folder)

    command_line_config.add_solution_modifications(matcher,
        active=in_problem_folder)

    command_line_config.add_import_opertions(matcher,
        active=not in_problem_folder)

    command_line_config.add_todo_operations(matcher,
        active=in_problem_folder)

    command_line_config.add_tags_operations(matcher,
        active=in_problem_folder)

    command_line_config.add_generate_operations(matcher,
        active=in_problem_folder)

    command_line_config.add_checking_solution_operations(matcher,
        active=in_problem_folder)

    command_line_config.add_computing_tl_functions(matcher,
        active=in_problem_folder)

    command_line_config.add_validate_operations(matcher,
        active=in_problem_folder)

    command_line_config.add_checker_operations(matcher,
        active=in_problem_folder)

    command_line_config.add_problem_config_modification_operations(matcher,
        active=in_problem_folder)

    command_line_config.add_zip_operation(matcher,
                                          active = in_problem_folder)

    command_line_config.add_stress_test_operations(matcher,
        active=in_problem_folder)

    command_line_config.add_contest_operations(matcher,
        active=not in_problem_folder)

    command_line_config.add_aggregate_operations(matcher,
        active=in_problem_folder)

    command_line_config.add_export_operations(matcher)

    command_line_config.add_easter_eggs_operations(matcher)

#    command_line_config.add_simple_bridge(matcher)

    if not command:
        logger.info("Type `please legacy commands' to show available"
                    "commands or `please legacy help' to show help")
        return
    try:
        matcher.matches(command)
    except MatcherException as ex:
        raise PleaseException('Legacy matcher error: {}'. format(ex))
    # other exceptions are handled above us


