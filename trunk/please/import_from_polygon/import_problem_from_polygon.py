from .import download_zip
from .import create_problem

def import_problem_from_polygon(contest_id, problem_letter):
    problem_name = download_zip.get_problem(int(contest_id), str(problem_letter).upper())

    print("__________________________________")
    print(problem_name + ".zip")
    print("__________________________________")
    create_problem.create_problem(problem_name + ".zip")