from . import create_problem
from . import polygon_unzip
from ..contest.contest import Contest
from ..contest import commands
import logging
import os
from lxml import etree
import shutil
from .lang_choice import make_language_choice
import re

def get_name_and_location_and_date(statement):
    regexp = r'.*\\contest.*{(?P<name>.*)}%.*{(?P<location>.*)}%.*{(?P<date>.*)}%'
    matched = re.match(regexp, statement, re.MULTILINE | re.DOTALL)
    name = matched.group('name')
    location = matched.group('location')
    date = matched.group('date')
    return name, location, date

def import_with_tree(tree, contest_path):
    cur_dir = os.getcwd()
    
    good_language_statement = make_language_choice(tree.xpath('names/name'))
    name = good_language_statement.get('value')
    language = good_language_statement.get('language')
    
    with open(os.path.join('statements', language, 'statements.tex'), 'r') as statement_file:
        statement = statement_file.read()
    
    os.chdir(contest_path)
    contest = Contest(name, ok_if_not_exists = True)
    name, date, location = get_name_and_location_and_date(statement)
    contest.config['statement']['name'] = name or ''
    contest.config['statement']['location'] = location or ''
    contest.config['statement']['date'] = date or ''
    
    importer = create_problem.PolygonProblemImporter()
    problems = tree.xpath('problems/problem')
    for problem in problems:
        problem_index = problem.get('index')
        problem_name = problem.get('name')
        importer.import_from_dir(os.path.join(cur_dir, 'problems', problem_name), contest_path)
        contest.problem_add(problem_name, problem_index)
    
    contest.config['name'] = name
    commands.write_contest(name, contest)
    os.chdir(cur_dir)

def import_from_dir(directory, contest_path):
    logger = logging.getLogger("please_logger.import_from_polygon.import_from_dir")
    
    prev_dir = os.getcwd()
    os.chdir(directory)
    
    tree = etree.parse('contest.xml').xpath('/contest')[0]
       
    name = make_language_choice(tree.xpath('names/name')).get('value')
    
    imported = False
    
    if not os.path.exists(os.path.join(contest_path, name + ".contest")):
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
    
