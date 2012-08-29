from please.command_line.template import Template

def add_generate_operations(matcher, active):
        from please.command_line.generate_tests import generate_tests, generate_tests_with_tags
        from please.latex import latex_tools
        from please.answers_generator.answers_generator import AnswersGenerator
        matcher.add_handler(Template(
                ["generate|gen", "tests", "with", "tag|tags", "@tags"]),
                generate_tests_with_tags, active)
        matcher.add_handler(Template(
                ["generate|gen", "tests"]),
                generate_tests, active)
        matcher.add_handler(Template(
                ["generate|gen", "statement|pdf"]),
                latex_tools.generate_problem, active)
        matcher.add_handler(Template(
                ["generate|gen", "answers|ans"]),
                AnswersGenerator.generate, active)

def add_validate_operations(matcher, active):
    from please.tests_answer_generator import tests_answer_generator
    from please.add_source.add_source import add_validator
    for tpl in [["validate|val", "tests"], ["validate"]]:
        matcher.add_handler(
            Template(tpl),
            tests_answer_generator.TestsAndAnswersGenerator().validate,
            active)
    matcher.add_handler(
        Template(["set", "validator|val", "$path"]),
        add_validator,
        active)

def add_stress_test_operations(matcher, active):
    from please import stress_tester
    from please.package import package_config
    pkg = package_config.PackageConfig.get_config()
    stresser = stress_tester.StressTester(config = pkg)
    matcher.add_handler(
        Template(["stress", "$solution", "$generator"]),
        stresser, 
        active)
    matcher.add_handler(
        Template(["stress", "$solution", "$correct_solution", "$generator"]),
        stresser,
        active)
    matcher.add_handler(
        Template(["stress", "$solution", "$generator", "with", "arg|args", "@args"]),
        stresser,
        active)
    matcher.add_handler(
        Template(["stress", "$solution", "$correct_solution", "$generator", "with", "arg|args", "@args"]),
        stresser,
        active)
 