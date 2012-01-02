from ..todo.todo_generator import TodoGenerator
from ..solution_tester.check_solution import check_multiple_solution
from ..solution_tester import package_config
from ..command_line.generate_tests import generate_tests
from ..latex import latex_tools
#from ..utils import cleanup

def build_all () :
    opened_config = package_config.PackageConfig.get_config()

    #run todo
    TodoGenerator.get_todo()

    #statement generation
    latex_tools.generate_contest()

    #run Tests And Answers Generator
    generate_tests()

    #run check soltuion
    check_multiple_solution()
