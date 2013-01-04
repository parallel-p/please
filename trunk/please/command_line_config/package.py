from please.command_line.template import Template
from please.zip import generate_zipfile

TL_ALIASES = "TL|tl|time-limit|timelimit|time_limit"
ML_ALIASES = "ML|ml|memory-limit|memorylimit|memory_limit"


def add_tags_operations(matcher, active):
    from please import tags
    for tpl in [["show", "tags"], ["tags"]]:
        matcher.add_handler(Template(tpl),
                tags.show_tags, active)
    matcher.add_handler(Template(["clear", "tags"]),
            tags.clear_tags, active)
    matcher.add_handler(Template(["add", "tag|tags", "@tags"]),
            tags.add_tags, active)


def add_computing_tl_functions(matcher, active):
    from please.auto_TL.auto_tl import set_integer_tl, set_float_tl
    matcher.add_handler(
        Template(["compute", TL_ALIASES]),
        set_float_tl,
        active)
    matcher.add_handler(
        Template(["compute", "integer", TL_ALIASES]),
        set_integer_tl,
        active)


def add_checker_operations(matcher, active):
    from please.checkers.standard_checkers_utils import add_standard_checker_to_solution
    from please.checkers.standard_checkers_utils import print_standard_checkers
    from please.add_source.add_source import add_checker
    matcher.add_handler(
            Template(["set", "standard|std", "checker", "#checker"]),
            add_standard_checker_to_solution, active)
    matcher.add_handler(
            Template(["set", "standard|std", "checker"]),
            print_standard_checkers,
            active)
    matcher.add_handler(
            Template(["set", "checker", "$path"]),
            add_checker,
            active)


def add_problem_config_modification_operations(matcher, active):
    import logging

    class SetParam:
        def __init__(self, arg_name):
            self.__arg_name = arg_name

        def __call__(self, value):
            log = logging.getLogger("please_logger.command_line_config")
            log.info("Set %s to %s in default.package" % (self.__arg_name, value))
            from please.package import package_config
            from please.utils.writepackage import writepackage
            opened_config = package_config.PackageConfig.get_config()
            opened_config[self.__arg_name] = value
            writepackage(opened_config.get_text())

    for tpl_list, arg_name in [
            (["name"], "name"),
            (["problem", "name"], "name"),
            (["input"], "input"),
            (["output"], "output"),
            ([TL_ALIASES], "time_limit"),
            ([ML_ALIASES], "memory_limit")]:
        matcher.add_handler(
            Template(["set"] + tpl_list + ["#value"]),
            SetParam(arg_name),
            active)


def add_zip_operation(matcher, active):
    matcher.add_handler(Template(['zip']), generate_zipfile, active)
