import os
import stat
import shutil
import subprocess

from .. import globalconfig
from ..log import logger
from ..globalconfig import svn, default_limits
from ..invoker.invoker import invoke, ExecutionLimits
from ..utils import platform_detector

svn_trash_dirs = ['.tests', '.statements']
svn_trash_mask = ['*.exe']

class SvnError(Exception):
    pass

def problem_in_svn(shortname = '.'):
    if globalconfig.svn['type'] == 'public':
        return os.path.exists(os.path.join(shortname, '.please', 'svn_path'))
    elif globalconfig.svn['type'] == 'personal':
        return os.path.exists('.svn')
    else:
        raise SvnError('svn repository type is unknown in globalconfig')        

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

def svn_command_with_star(command):
    #if command include *, it must be run with bash under unix
    #TODO check for MAC
    if platform_detector.get_platform()[0] == 'Windows':
        return ['svn'] + command + ['--username', svn['username'],
                                    '--password', svn['password']]
    else:
        return ['bash', '-c', " ".join(['svn'] + command + ['--username', 
                svn['username'], '--password', svn['password']])]


def svn_operation(command):
    #all real communication with svn is in this function only
    if svn['url'] != '':
        #check if svn path exist:
        if command[0] == 'ls':
            run_command = ['svn'] + command + ['--username', svn['username'],
                                                        '--password', svn['password']]
            result = 1 - subprocess.call(run_command)
            return result
        else:
            logger.info("svn " + " ".join(command))
            result = 1 - subprocess.call(svn_command_with_star(command))
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
                   '-m', '"create directory for new problem ' + shortname + '"'])

    # 2. Checkout it into local problem directory
    svn_operation(['checkout', svn['url'] + svnname, shortname])

    # 3. Add all content of this directory to svn
    os.chdir(shortname)
    svn_operation(['add', '*'])

    # 4. Commit
    svn_operation(['ci', '-m', '"problem ' + shortname + ' initial commit"'])
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
                   '--parents', '-m', '"move problem ' + shortname + ' to .deleted"'])
    shutil.rmtree(shortname, onerror = on_remove_error)

class ProblemInSvn:
    '''Main purpose of this class - to exclude double checks of svn accessibility
       and duplicating svn up command

       USAGE for public svn:
       ProblemInSVN().add('checker.cpp', 'checker')
       ProblemInSVN().update('solutions/solution.cpp', 'solution')
       ProblemInSVN().update('default.please')

       USAGE for personal svn:
       ProblemInSVN().sync()
    '''

    __in_svn = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ProblemInSvn, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        #run from problem directory
        if self.__in_svn is None and globalconfig.svn['type'] == 'public':
            print('*********')
            if not problem_in_svn():
                logger.warning("Problem is not in svn repository")
                #raise SvnError
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
        if globalconfig.svn['type'] == 'public' and self.__in_svn:
            svn_operation(['add', path])
            svn_operation(['ci', '-m', '"' + description + ' ' + path + ' added"'])

    def update(self, path, description = ''):
        #run from problem directory
        if globalconfig.svn['type'] == 'public' and self.__in_svn:
            svn_operation(['ci', '-m', '"' + description + ' ' + path + ' updated"'])

    def sync():
        '''for personal svn
           0. svn up
           1. svn add all 
           2. revert trash dirs
           3. revert trash files
           4. commit
        '''
        if globalconfig.svn['type'] == 'personal' and self.__in_svn:
            svn_operation(['up'])
            svn_operation(['add', '*'])
            svn_operation(['revert', svn_trash_dirs])
            for (directory, tmp, tmp2) in os.walk('.'):
                svn_operation(['revert', list(map(lambda x: os.path.join(directory, x), svn_trash_mask))])            
            svn_operation(['ci', '-m', '" "'])
        