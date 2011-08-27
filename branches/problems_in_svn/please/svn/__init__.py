import os
import stat
import shutil
import psutil
from subprocess import PIPE

from ..log import logger
from ..globalconfig import svn, default_limits
from ..invoker.invoker import invoke, ExecutionLimits

def svn_probname(shortname):
    user = svn['username'].split('@')[0]
    return shortname + '_' + user 

def get_svn_path(shortname):
    with open(os.path.join(shortname, '.please', 'svn_path'),
                                        'r', encoding='utf-8') as f:
        return f.readline()

def get_svn_name(shortname):
    with open(os.path.join(shortname, '.please', 'svn_name'),
                                        'r', encoding='utf-8') as f:
        return f.readline()

def svn_operation(command):
    #all real communication with svn is in this function only
    if svn['url'] != '':
        handler = psutil.Popen(['svn'] + command + ['--username', svn['username'], 
                                                    '--password', svn['password']],
                               stdout = PIPE) 
        result = invoke(handler, default_limits)
        if result.verdict == 'OK':
            logger.info("svn " + " ".join(command)) 
        else:
            logger.error("failed: svn " + " ".join(command))
            exit()
        return result

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
    shutil.rmtree(shortname, onerror = on_remove_error)
    if svn['url'] != '':
        svn_path = get_svn_path(shortname)
        svn_name = get_svn_name(shortname)
        svn_operation(['move', svn_path + '/' + svn_name,
                           svn_path + '/.deleted/' + svn_name,
                   '--parents', '-m', 'move problem ' + shortname + ' to .deleted'])

