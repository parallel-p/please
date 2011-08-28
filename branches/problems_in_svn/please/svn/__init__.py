import os
import stat
import shutil
import subprocess

from ..executors import runner
from ..log import logger
from ..globalconfig import svn, default_limits
from ..invoker.invoker import invoke, ExecutionLimits

class SvnError(Exception):
    pass

def problem_in_svn(shortname = '.'):
    return os.path.exists(os.path.join(shortname, '.please', 'svn_path'))

def svn_probname(shortname):
    user = svn['username'].split('@')[0]
    return shortname + '_' + user + '_' + str(int(float(get_time_config(shortname))))

def get_svn_path(shortname = '.'):
    with open(os.path.join(shortname, '.please', 'svn_path'),
                                        'r', encoding='utf-8') as f:
        return f.readline()

def get_svn_name(shortname = '.'):
    with open(os.path.join(shortname, '.please', 'svn_name'),
                                        'r', encoding='utf-8') as f:
        return f.readline()

def get_time_config(shortname):
    with open(os.path.join(shortname, '.please', 'time.config'),
                                        'r', encoding='utf-8') as f:
        return f.readline()

def svn_accessible(shortname = '.'):
    return svn_path_exists(get_svn_path(shortname))

def svn_path_exists(path):
    result = svn_operation(['ls', path, '--depth=empty'])
    #print(result)
    return result

def svn_problem_exists(shortname = '.'):
    return svn_path_exists(get_svn_path(shortname) + '/' + get_svn_name(shortname))

def svn_deleted_problem_exists(shortname = '.'):
    return svn_path_exists(get_svn_path(shortname) + '/.deleted/' + get_svn_name(shortname))

def svn_operation(command):
    #all real communication with svn is in this function only
    if svn['url'] != '':
        #check if svn path exist:
        if command[0] == 'ls':
            run_command = ['svn'] + command + ['--username', svn['username'], 
                                                        '--password', svn['password']]
            #print(run_command)
            result = 1 - subprocess.call(run_command)
            return result
        else:
            logger.info("svn " + " ".join(command)) 
            run_command = ['svn'] + command + ['--username', svn['username'], 
                                                        '--password', svn['password']]
            result = 1 - subprocess.call(run_command)
            if result:
                return True
            else:
                logger.error("failed: svn " + " ".join(command))
                raise SvnError("failed: svn " + " ".join(command))

def add_created_problem(shortname):
    shortname = str(shortname)
    svnname = svn_probname(shortname)

    # 0. Create .please/svn_path and write down svn path;
    # create .please/svn_name and write down svn problem directory;
    with open(os.path.join(shortname, '.please', 'svn_path'),
              'w', encoding='utf-8') as f:
        f.write(svn['url'])
    with open(os.path.join(shortname, '.please', 'svn_name'),
              'w', encoding='utf-8') as f:
        f.write(svnname)

    # 1. Create empty directory in svn
    # --parents creates directory 'problems', if it doesn't exist
    svn_operation(['mkdir', svn['url'] + svnname, '--parents',
                   '-m', 'create directory for new problem ' + shortname])

    # 2. Checkout it into local problem directory
    svn_operation(['checkout', svn['url'] + svnname, shortname])

    # 3. Add all content of this directory to svn
    os.chdir(shortname)
    svn_operation(['add', '*']) 

    # 4. Commit
    svn_operation(['ci', '-m', 'problem ' + shortname + ' initial commit'])
    os.chdir('..')

def on_remove_error(func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it: 
    # it's usually .svn/all-wcprops
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)

def delete_problem(shortname):
    if svn['url'] != '':
        svn_path = get_svn_path(shortname)
        svn_name = get_svn_name(shortname)
        svn_operation(['move', svn_path + '/' + svn_name,
                           svn_path + '/.deleted/' + svn_name,
                   '--parents', '-m', 'move problem ' + shortname + ' to .deleted'])
    shutil.rmtree(shortname, onerror = on_remove_error)

class ProblemInSvn:
    '''Main purpose of this class - to exclude double checks of svn accessibility
       and duplicating svn up command

       USAGE:
       in_svn = ProblemInSVN()
       in_svn.add('checker.cpp', 'checker')
       in_svn.update('solutions/solution.cpp', 'solution')
       in_svn.update('default.please')
    '''   

    def __init__(self):
        #run from problem directory
        if not problem_in_svn():
            logger.warning("Problem is not in svn repository")
            self.__in_svn = False
        elif not svn_accessible():
            logger.warning("No access to svn. Please, commit your changes manually later")
            self.__in_svn = False
        elif not svn_problem_exists():
            if svn_deleted_problem_exists():
                logger.warning("Problem was deleted and moved to .deleted folder in svn")
                self.__in_svn = False
            else:
                logger.error("Problem was not found in svn")
                self.__in_svn = False
        else:
            logger.info("Problem found in svn")
            self.__in_svn = True
            svn_operation(['up'])

    def add(self, path, description = ''):
        #run from problem directory
        if self.__in_svn:
            svn_operation(['add', path])
            svn_operation(['ci', '-m', description + ' ' + path + ' added'])

    def update(self, path, description = ''):
        #run from problem directory
        if self.__in_svn:
            svn_operation(['ci', '-m', description + ' ' + path + ' updated'])
             