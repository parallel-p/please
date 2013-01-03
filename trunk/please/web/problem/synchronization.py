from please.package.package_config import PackageConfig
from please import globalconfig
from please.add_source.add_source import add_solution
from problem.models import ProblemTag, WellDone, Solution, Verdict

def import_to_database(model, path=None, name=globalconfig.default_package):
    conf = PackageConfig.get_config(path or str(model.path), name)

    model.name = conf.get("name", "")
    model.short_name = conf.get("shortname", "")

    model.tags.clear()
    for entry in conf.get('tags', '').split(';'):
        model.tags.add(ProblemTag.objects.get_or_create(name=entry.strip())[0])

    model.input = conf.get("input", "")
    model.output = conf.get("output", "")
    model.time_limit = float(conf.get("time_limit", "2.0"))
    model.memory_limit = int(conf.get("memory_limit", "268435456"))

    model.checker_path = conf.get("checker", "")
    model.validator_path = conf.get("validator", "")

    model.statement_path = conf.get("statement", "")
    model.description_path = conf.get("description", "")
    model.analysis_path = conf.get("analysis", "")

    model.hand_answer_extension = conf.get("hand_answer_extension", "")
    print(model.hand_answer_extension)

    model.well_done_test.clear()
    for entry in conf.get('well_done_test', []):
        model.well_done_test.add(WellDone.objects.get_or_create(name=entry)[0])
    
    model.well_done_answer.clear()
    for entry in conf.get('well_done_answer', []):
        model.well_done_answer.add(WellDone.objects.get_or_create(name=entry)[0])

    for solution in conf.get("solution", []):
        sol = Solution.objects.get_or_create(path=solution['source'], problem=model)[0]
        sol.input = solution.get('input')
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


def export_from_database(model, name=globalconfig.default_package):
    conf = PackageConfig.get_config(str(model.path), name)
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
    conf['well_done_test'] = map(lambda well_done: well_done.name, model.well_done_test.all())
    conf['well_done_answer'] = map(lambda well_done: well_done.name, model.well_done_answer.all())
    conf['analysis'] = str(model.analysis_path)
    conf.write()
    for solution in model.solution_set.all():
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
        add_solution(str(solution.path), args, root_dir=str(model.path))
