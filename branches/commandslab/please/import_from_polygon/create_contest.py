import logging
import os
import shutil
import re
from .lang_choice import make_language_choice
from .create_problem import PolygonProblemImporter
from . import polygon_unzip
from ..contest.contest import Contest
from ..contest import commands
from xml.etree.ElementTree import ElementTree

def get_name_and_location_and_date(statement):
    regexp = r'.*\\contest.*{(?P<name>.*)}%.*{(?P<date>.*)}%.*{(?P<location>.*)}%'
    matched = re.match(regexp, statement, re.MULTILINE | re.DOTALL)
    name = matched.group('name')
    location = matched.group('location')
    date = matched.group('date')
    return name, location, date

def import_with_tree(tree, contest_path):
    cur_dir = os.getcwd()
    good_language_statement = make_language_choice(tree.findall('names/name'))
    name = good_language_statement.get('value')
    language = good_language_statement.get('language')
    
    with open(os.path.join('statements', language, 'statements.tex'), 'r', encoding = 'utf-8') as statement_file:
        statement = statement_file.read()
    
    os.chdir(contest_path)
    contest = Contest(commands.get_contest_config(name), ok_if_not_exists = True)
    name, date, location = get_name_and_location_and_date(statement)
    contest.config['statement']['name'] = name or ''
    contest.config['statement']['location'] = location or ''
    contest.config['statement']['date'] = date or ''
    
    importer = PolygonProblemImporter()
    problems = tree.findall('problems/problem')
    for problem in problems:
        problem_index = problem.get('index')
        problem_name = problem.get('url').split('/')[-1]
        importer.import_from_dir(os.path.join(cur_dir, 'problems', problem_name), contest_path)
        contest.problem_add(problem_name, problem_index)
    
    contest.config['name'] = name
    commands.write_contest(commands.get_contest_config(name), contest)
    os.chdir(cur_dir)

def import_from_dir(directory, contest_path):
    logger = logging.getLogger("please_logger.import_from_polygon.import_from_dir")
    
    prev_dir = os.getcwd()
    os.chdir(directory)
    
    tree = ElementTree().parse('contest.xml')
       
    name = make_language_choice(tree.findall('names/name')).get('value')
    
    imported = False
    
    if not os.path.exists(os.path.join(contest_path, commands.get_contest_config(name))):
        import_with_tree(tree, contest_path)
        imported = True
    else:
        logger.error("Import error: %s already exists" % name)
    
    os.chdir(prev_dir)
    
    if imported:
        logger.warning('Imported polygon contest %s' % name)

def create_contest(name):
    prev_dir = os.getcwd()
    
    path, file_name = os.path.split(name)
    
    if path != "":
        os.chdir(path)
    
    directory = '.' + os.path.splitext(file_name)[0]
    polygon_unzip.unzip(file_name, directory)
    
    import_from_dir(directory, prev_dir)
    
    shutil.rmtree(directory)
    
    os.chdir(prev_dir)
    
