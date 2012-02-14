from ..todo.todo_generator import TodoGenerator
from ..solution_tester.check_solution import check_all_solutions
from ..solution_tester import package_config
from ..command_line.generate_tests import generate_tests
from ..latex import latex_tools
from ..reports import generate_html_report
#from ..utils import cleanup

def build_all () :
    opened_config = package_config.PackageConfig.get_config()
    # TODO: check if opened_config is None
    # opened_config is unused here, remove it

    #run todo
    TodoGenerator.get_todo()

    #statement generation
    latex_tools.generate_problem()

    #run Tests And Answers Generator
    generate_tests()

    #run check soltuion
    check_all_solutions()

    #generate_html_report.generate_html_report()
