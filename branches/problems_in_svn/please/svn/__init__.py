from os import chdir
import psutil
from subprocess import PIPE

from ..log import logger
from ..globalconfig import svn, default_limits
from ..invoker.invoker import invoke, ExecutionLimits

def get_svnname(shortname):
    user = svn['username'].split('@')[0]
    return shortname + '_' + user 

def svn_operation(command):
    handler = psutil.Popen(['svn'] + command + ['--username', svn['username'], 
                                      '--password', svn['password']],
                           stdout = PIPE) 
    #print(" ".join(['svn'] + command + ['--username', svn['username'], 
    #                                  '--password', svn['password']]))
    result = invoke(handler, default_limits)
    if result.verdict == 'OK':
        logger.info(" ".join(command)) 
    else:
        logger.error("failed " + " ".join(command))
        exit()
    return result

def add_created_problem(shortname):
    shortname = str(shortname)
    svnname = get_svnname(shortname)

    # 1. Create empty directory in svn
    # --parents creates directory 'problems', if it doesn't exist
    svn_operation(['mkdir', svn['url'] + svnname, '--parents',
                   '-m', 'create directory for new problem ' + shortname])

    # 2. Checkout it into local problem directory
    svn_operation(['checkout', svn['url'] + svnname, shortname])

    # 3. Add all content of this directory to svn
    chdir(shortname)
    svn_operation(['add', '*']) 

    # 4. Commit
    svn_operation(['ci', '-m', 'problem ' + shortname + ' initial commit'])
    chdir('..')

