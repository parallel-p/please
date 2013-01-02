from please.package.package_config import PackageConfig
from please import globalconfig
from please.add_source.add_source import add_solution


def import_to_database(model, path=None, name=globalconfig.default_package):
    conf = PackageConfig.get_config(path, name)

    model.name = conf["name"]
    model.short_name = conf["shortname"]
    model.type = ''
    
    model.input = conf["input"]
    model.output = conf["output"]
    model.time_limit = float(conf["time_limit"])
    model.memory_limit = int(conf["memory_limit"])

    model.checker = conf["checker"]
    model.validator = conf["validator"]
    model.main_solution = conf["main_solution"]

    model.statement = conf["statement"]
    model.description = conf["description"]

    model.hand_answer_extension = conf["hand_answer_extension"]

    model.well_done_test = conf["well_done_test"]
    model.well_done_answer = conf["well_done_answer"]
                                   
    model.analysis = conf["analysis"]

def export_from_database(model, name=globalconfig.default_package):
	conf = PackageConfig.get_config(str(model.path), name)
	conf.name = str(model.name)
	conf.shortname = str(model.short_name)
	conf.tags = ', '.join(map(str, model.tags.all()))
	conf.type = ''
	conf.input = str(model.input)
	conf.output = str(model.output)
	conf.time_limit = str(model.time_limit)
	conf.memory_limit = str(model.memory_limit)
	conf.checker = str(model.checker_path)
	conf.validator = str(model.validator_path)
	conf.main_solution = str(model.main_solution.path)
	conf.statement = str(model.statement_path)
	conf.description = str(model.description_path)
	conf.hand_answer_extension = str(model.hand_answer_extension)
	conf.well_done_test = str(model.well_done_test)
	conf.well_done_answer = str(model.well_done_answer)
	conf.analysis = str(model.analysis_path)
	conf.write()
	for solution in model.solution_set.all():
		args = []
		if solution.path_or_stdin:
			args += ['input', str(solution.input)]
		if solution.path_or_stdout:
			args += ['output', str(solution.output)]
		if solution.possible_verdicts.count() != 0:
			args += (['possible'] +
			        list(map(str, solution.possible_verdicts.all())))
		if solution.expected_verdicts.count() != 0:
			args += (['expected'] +
			        list(map(str, solution.expected_verdicts.all())))
		add_solution(str(solution.filename), args)
