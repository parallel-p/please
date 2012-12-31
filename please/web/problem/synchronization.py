from please.package.config import Config
import os

def import_to_database(path):
    os.chdir(path)
    config = Config(open("default.package", "r").read())
    return config

def import_from_database(model, path):
	cpath = os.getcwd()
	os.chdir(path)
	conf = Config()
	conf.name = str(model.name)
	conf.shortname = str(model.short_name)
	conf.set('tags', list(map(str, model.tags.all())), in_list=True)
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
