from ...package.package_config import get_config
from ... import globalconfig
from ...add_source.add_source import add_solution


def import_from_database(model, path=None, name=globalconfig.default_package):
	conf = get_config(path, name)
	conf.name = str(model.name)
	conf.shortname = str(model.short_name)
	conf.set('tags', list(map(str, model.tags.all())))
	conf.type = ''
	conf.input = str(model.input)
	conf.output = str(model.output)
	conf.time_limit = str(model.time_limit)
	conf.memory_limit = str(model.memory_limit)
	conf.checker = str(model.checker)
	conf.validator = str(model.validator)
	conf.main_solution = str(model.main_solution)
	conf.statement = str(model.statement)
	conf.description = str(model.description)
	conf.hand_answer_extension = str(model.hand_answer_extension)
	conf.well_done_test = str(model.well_done_test)
	conf.well_done_answer = str(model.well_done_answers)
	conf.analysis = str(model.analysis)
	conf.write()
	for solution in model.solution_set.all():
		args = []
		if solution.path_or_stdin:
			args += ['input', str(solution.path_or_stdin)]
		if solution.path_or_stdout:
			args += ['output', str(solution.path_or_stdout)]
		if solution.possible_verdicts.count() != 0:
			args += (['possible'] +
			        list(map(str, solution.possible_verdicts.all())))
		if solution.expected_verdicts.count() != 0:
			args += (['expected'] +
			        list(map(str, solution.expected_verdicts.all())))
		add_solution(str(solution.filename), args)
