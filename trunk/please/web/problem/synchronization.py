from please.package.package_config import PackageConfig
from please import globalconfig
from please.add_source.add_source import add_solution
from django.core.exceptions import FieldError


def import_to_database(model, path=None, name=globalconfig.default_package):
    conf = PackageConfig.get_config(path or str(model.path), name)

    model.name = conf["name"]
    model.short_name = conf["shortname"]

    model.tags.clear()
    for entry in conf['tags']:
    	try:
    	    ctag = ProblemTag.objects.get(name=entry)
    	except FieldError:
    		ctag = ProblemTag(name=entry)
    		ctag.save()
    	model.tags.add(ctag)

    model.input = conf["input"]
    model.output = conf["output"]
    model.time_limit = float(conf["time_limit"])
    model.memory_limit = int(conf["memory_limit"])

    model.checker_path = conf["checker"]
    model.validator_path = conf["validator"]

    model.statement_path = conf["statement"]s
    model.description_path = conf["description"]
    model.analysis_path = conf["analysis"]

    model.hand_answer_extension = conf["hand_answer_extension"]

    model.well_done_test.clear()
    for entry in conf['well_done_test'].split(', '):
    	model.well_done_test.add(WellDone.objects.get(name=entry))
    
    model.well_done_answer.clear()
    for entry in conf['well_done_answer'].split(', '):
    	model.well_done_answer.add(WellDone.objects.get(name=entry))

    for solution in conf["solution"]:
    	try:
    		sol = Solution.objects.get(path=solution['source'], problem=model)
    		sol.input = solution['input']
    		sol.output = solution['output']
    		sol.expected_verdicts.clear()
    		for verdict in solution['expected']:
    			sol.expected_verdicts.add(Verdict.objects.get(name=verdict))
    		sol.possible_verdicts.clear()
    		for verdict in solution['possible']:
    			sol.possible_verdicts.add(Verdict.objects.get(name=verdict))
    	except FieldError:  # Let us create this solution, then...
    		sol = Solution(
    			path=solution['source'],
    			problem=model,
    			input=solution['input'],
    			output=solution['output']
    		)
    		for verdict in solution['expected']:
    			sol.expected_verdicts.add(Verdict.objects.get(name=verdict))
    		for verdict in solution['possible']:
    			sol.possible_verdicts.add(Verdict.objects.get(name=verdict))
    	if solution['source'] == conf['main_solution']:
    		model.main_solution = sol
    	sol.save()

    model.save()


def export_from_database(model, name=globalconfig.default_package):
    conf = PackageConfig.get_config(str(model.path), name)
    conf['name'] = str(model.name)
    conf['shortname'] = str(model.short_name)
    conf['tags'] = ', '.join(map(str, model.tags.all()))
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
    conf['well_done_test'] = str(model.well_done_test)
    conf['well_done_answer'] = str(model.well_done_answer)
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
        add_solution(str(solution.path), args)
