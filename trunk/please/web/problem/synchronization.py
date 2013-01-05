from please.package.package_config import PackageConfig
from please.package.config import ConfigFile
from please import globalconfig
from please.add_source.add_source import add_solution, del_solution
from problem.models import Problem, ProblemTag, WellDone, Solution, Verdict
from problem.views.file_utils import ChangeDir
from please.utils.exceptions import PleaseException
from please import launcher
import os


def import_to_database(model=Problem(), path=None, name=globalconfig.default_package):
    if path is not None:
        try:
            model = Problem.objects.get(path=path)
        except Problem.DoesNotExist:
            if path[-1] == os.sep:
                path = path[:-1]
            else:
                path += os.sep
            model = Problem.objects.get_or_create(path=path)[0]

    problem_path = path or str(model.path)

    if not os.path.exists(problem_path):
        print('Deleting model')
        model.delete()
        return

    conf = PackageConfig.get_config(problem_path, name)

    model.name = conf.get("name", "")
    model.short_name = conf.get("shortname", "")

    model.tags.clear()
    for entry in conf.get('tags', '').split(';'):
        if entry.strip() != '':
            model.tags.add(ProblemTag.objects.get_or_create(name=entry.strip())[0])

    model.input = conf.get("input", "")
    model.output = conf.get("output", "")
    model.time_limit = float(conf.get("time_limit", "2.0"))
    model.memory_limit = int(conf.get("memory_limit", "268435456"))

    model.checker_path = os.path.relpath(conf.get("checker", ""), os.path.abspath(problem_path)) if conf.get("checker", "") != "" else ""
    model.validator_path = conf.get("validator", "")

    model.statement_path = conf.get("statement", "")
    model.description_path = conf.get("description", "")
    model.analysis_path = conf.get("analysis", "")

    model.hand_answer_extension = conf.get("hand_answer_extension", "")

    model.well_done_test.clear()
    for entry in conf.get('well_done_test', []):
        model.well_done_test.add(WellDone.objects.get_or_create(name=entry)[0])

    model.well_done_answer.clear()
    for entry in conf.get('well_done_answer', []):
        model.well_done_answer.add(WellDone.objects.get_or_create(name=entry)[0])

    for solution in conf.get("solution", []):
        sol = Solution.objects.get_or_create(path=solution['source'], problem=model)[0]
        if 'input' in solution:
            sol.input = solution.get('input')
        if 'output' in solution:
            sol.output = solution.get('output')
        sol.expected_verdicts.clear()
        sol.possible_verdicts.clear()
        for verdict in solution['expected']:
            sol.expected_verdicts.add(Verdict.objects.get_or_create(name=verdict)[0])
        for verdict in solution.get('possible'):
            sol.possible_verdicts.add(Verdict.objects.get_or_create(name=verdict)[0])
        if solution['source'] == conf['main_solution']:
            model.main_solution = sol
        sol.save()

    model.save()
    return model


def export_from_database(model, name=globalconfig.default_package):
    with ChangeDir(str(model.path)):
        try:
            conf = PackageConfig.get_config('.', name)
        except TypeError:  # Seemingly, this is due to a lacking please_verion.
            conf = ConfigFile(name)
        conf['please_version'] = conf['please_version'] or str(globalconfig.please_version)
        conf['name'] = str(model.name)
        conf['shortname'] = str(model.short_name)
        conf['tags'] = '; '.join(map(str, model.tags.all()))
        conf['type'] = ''
        conf['input'] = str(model.input)
        conf['output'] = str(model.output)
        conf['time_limit'] = str(model.time_limit)
        conf['memory_limit'] = str(model.memory_limit)
        conf['checker'] = str(model.checker_path)
        conf['validator'] = str(model.validator_path)
        if model.main_solution is not None:
            conf['main_solution'] = str(model.main_solution.path)
        conf['statement'] = str(model.statement_path)
        conf['description'] = str(model.description_path)
        conf['hand_answer_extension'] = str(model.hand_answer_extension)
        conf['well_done_test'] = list(map(lambda well_done: well_done.name, model.well_done_test.all()))
        conf['well_done_answer'] = list(map(lambda well_done: well_done.name, model.well_done_answer.all()))
        conf['analysis'] = str(model.analysis_path)
        conf.write()

        sources = []
        already_there = [x['source'].replace(os.sep, '/') for x in conf['solution']]
        for solution in model.solution_set.all():
            solution.path = solution.path.replace(os.sep, '/')
            sources.append(str(solution.path))
            if str(solution.path) in already_there:
                continue
            args = []
            if solution.input:
                args += ['input', str(solution.input)]
            if solution.output:
                args += ['output', str(solution.output)]
            if solution.possible_verdicts.count() != 0:
                args += (['possible'] +
                        list(map(str, solution.possible_verdicts.all())))
            if solution.expected_verdicts.count() != 0:
                args += (['expected'] +
                        list(map(str, solution.expected_verdicts.all())))
            try:
                add_solution(str(solution.path), args)
            except PleaseException:
                solution.delete()
        for sol in already_there:
            if (sol not in sources) and (sol != conf['main_solution'].replace(os.sep, '/')):
                del_solution(sol)


def import_tree(path):
    paths = []
    for root, dirs, files in os.walk(path):
        package = PackageConfig.get_config(root)
        if package:
            paths.append(root)
            problem = Problem(path=root)
            problem.save()
            import_to_database(problem)
            problem.save()
    return paths
