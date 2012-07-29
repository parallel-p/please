# -*- coding: utf-8 -*-
from please import globalconfig
from please.package import config
from please.package.package_config import PackageConfig
from please.export2ejudge.connect_to_server import Connector
import os
import re
import shutil
import zipfile
import distutils.archive_util
    
serve_problem_template_name = os.path.join(globalconfig.root, 'export2ejudge', 'serve_problem_template.part')
global test_sfx
global corr_sfx

ignoring_dirs = ['.svn']

def is_text(filename):
    '''
    Heuristic check, that file is text, not binary
    '''
    #read first several bytes
    with open(filename, 'rb') as file:
        s = str(file.read(512))
    text_characters = "".join(list(map(chr, range(32, 255))) + list("\n\r\t\b"))
    if "\0" in (s):
        return False
    if not s:  # Empty files are considered text 
        return True

    t = ''.join(filter(lambda x: not ((x) in text_characters), s))
    # If more than 30% non-text characters, then 
    # this is considered a binary file 
    if len(t)/len(s) > 0.30:
        return False
    return True
    
def without_extention(path):
    return re.match(r'(.*)\..*', os.path.basename(path)).groups()[0]

def recreate_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    
def prepare_tests(path):
    tests = []
    corrs = []
    tests_dict = {}
    corrs_dict = {}
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            if file.endswith('.a'):
                corrs.append(file)
            else:
                tests.append(file)
    
    
    #max_len = 0
    #for s in tests:
    #    max_len = max(max_len, len(s))
    
    max_len = 2
        
    for i in range(len(tests)):
        tests_dict[os.path.join(path, tests[i])] = tests[i].zfill(max_len)
        
    for i in range(len(corrs)):
        corrs_dict[os.path.join(path, corrs[i])] = corrs[i].zfill(max_len + len(os.path.splitext(corrs[i])))
        
    return (tests_dict, corrs_dict, max_len)
    
def get_text_files_from_dir(path):
    for file in os.listdir(path):
        if os.path.isfile(path):
            if is_text(os.path.join(path, file)):
                yield file
            
def recursive_zip(zipf, directory, folder=None):
    nodes = os.listdir(directory)
    for item in nodes:
        if not (item in ignoring_dirs):
            full_item = os.path.join(directory, item)
            if os.path.isfile(full_item):
                zipf.write(full_item, folder, zipfile.ZIP_DEFLATED)
            elif os.path.isdir(item):
                recursive_zip(zipf, os.path.join(directory, item), os.path.join(folder, item))
    
def export_problem2ejudge(contest_path, task, problem_id):
    problem_config = PackageConfig.get_config(task)
    with open(serve_problem_template_name, 'r') as serve_template_file:
        serve_problem_template = serve_template_file.readlines()
    
    tests_info = prepare_tests(os.path.join(task, '.tests'))
    
    replaces = {'$id$': str(problem_id),
                '$shortname$': problem_config['shortname'],
                '$longname$': problem_config['name'],
                '$internalname$': problem_config['shortname'],
                '$inputfile$': problem_config['input'],
                '$outputfile$': problem_config['output'],
                '$timelimit_ms$': str(round(float(problem_config['time_limit'])*1000)),
                '$memorylimit_kb$': str(round(float(problem_config['memory_limit'])*1024)),
                '$checker$': without_extention(problem_config['checker']),
                '$testnamelen$': r"%02d" % tests_info[2]}

    if os.path.join(globalconfig.root, globalconfig.checkers_dir) in problem_config['checker']:
        try:
            checker_dir = os.path.join(globalconfig.root, globalconfig.checkers_dir)
            shutil.copy(os.path.join(problem_config['checker']), os.path.join(task, os.path.split(problem_config['checker'])[1]))
            shutil.copy(os.path.join(checker_dir,'testlib.h'), os.path.join(task, 'testlib.h'))
        except:
            pass

    for replace in replaces:
        lambda_replace = lambda x : x.replace(replace, replaces[replace])
        serve_problem_template = list(map(lambda_replace, serve_problem_template))

    summary_serve_problem = []

    for line in serve_problem_template:
        re_find = re.match('!(.*)!(.*)', line)
        if not re_find:
            summary_serve_problem.append(line)
        elif eval(re_find.groups()[0]):
            summary_serve_problem.append(re_find.groups()[1]+'\n')

    serve_cfg_path = os.path.join(contest_path, 'conf', 'serve.cfg')
    with open(serve_cfg_path, 'a') as serve_file:
        serve_file.writelines(summary_serve_problem)
    
    problem_path = os.path.join(contest_path, 'problems', task)
    os.mkdir(problem_path)
    
    problem_tests_dir = os.path.join(problem_path, 'tests')
    os.mkdir(problem_tests_dir)
    
    for file in tests_info[0]:
        shutil.copy(file, os.path.join(problem_tests_dir, tests_info[0][file]))
    
    for file in tests_info[1]:
        shutil.copy(file, os.path.join(problem_tests_dir, tests_info[1][file]))
        
    os.mkdir(os.path.join(problem_path, 'statements'))
    for file in get_text_files_from_dir(os.path.join(task, 'statements')):
        shutil.copy(os.path.join(task, 'statements', file), os.path.join(problem_path, 'statements', file))
        
    for file in filter(lambda x : os.path.isfile(os.path.join(task, x)), os.listdir(task)):
        if is_text(os.path.join(task, file)):
            shutil.copy(os.path.join(task, file), os.path.join(problem_path, file))

def export2ejudge(contest_id, tasks):
    export_path = '.export2ejudge'
    recreate_dir(export_path)
    
    config_path = os.path.join(export_path, 'serve.cfg')
    ejudge_server = Connector(globalconfig.ejudge_host, globalconfig.ejudge_port, globalconfig.ejudge_login, globalconfig.ejudge_password)
    ejudge_server.download_file(globalconfig.ejudge_contests_dir + ("%06d" % int(contest_id)) + "/conf/serve.cfg", config_path)
    
    
    contest_path = os.path.join(export_path,contest_id)
    recreate_dir(contest_path)
    serve_cfg_path = os.path.join(contest_path, 'conf', 'serve.cfg')
    recreate_dir(os.path.join(contest_path, 'conf'))
    with open(config_path, 'r') as config_file:
        serve_cfg_text = config_file.readlines()
    
    i = 0
    abstracts = []
    while i < len(serve_cfg_text):
        while (i < len(serve_cfg_text)) and not('[problem]' in serve_cfg_text[i]):
            i += 1
        current_deleting = []
        is_abstract = False
        if (i < len(serve_cfg_text)):
            current_deleting += serve_cfg_text.pop(i)
        while (i < len(serve_cfg_text)) and (serve_cfg_text[i][0] != '['):
            if serve_cfg_text[i].strip() == 'abstract':
                is_abstract |= True
            current_deleting += serve_cfg_text.pop(i)
        if is_abstract:
            abstracts += current_deleting
    
    serve_cfg_text += abstracts
   
    with open(serve_cfg_path, 'w') as serve_file: 
        serve_file.writelines(serve_cfg_text)
    
    try:
        shutil.rmtree(os.join(contest_path, 'problems'))
    except:
        pass
    os.mkdir(os.path.join(contest_path, 'problems'))

   
    for problem_id in range(len(tasks)):
        export_problem2ejudge(contest_path, tasks[problem_id], problem_id + 1)

    os.chdir(export_path)
    zip_name = "%06d.zip" % int(contest_id)
    distutils.archive_util.make_zipfile("%06d" % int(contest_id), contest_id)
    ejudge_server.upload_file(zip_name, globalconfig.ejudge_contests_dir + "%06d.zip" % int(contest_id))
