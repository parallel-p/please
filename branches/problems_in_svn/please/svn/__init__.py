from os import chdir
import psutil
from subprocess import PIPE

from ..log import logger
from ..globalconfig import svn, default_limits
from ..invoker.invoker import invoke, ExecutionLimits

def svn_operation(command):
    handler = psutil.Popen(['svn'] + command + ['--username', svn['username'], 
                                      '--password', svn['password']],
                           stdout = PIPE) 
    result = invoke(handler, default_limits)
    logger.info(" ".join(command)) 



def add_created_problem(shortname):
    shortname = str(shortname)

    # 1. Create empty directory in svn
    svn_operation(['mkdir', 
                   svn['url'] + shortname,
                   '-m', 'create directory for new problem ' + shortname])

    # 2. Checkout it into local problem directory
    svn_operation(['checkout', 
                   svn['url'] + shortname, shortname])

    # 3. Add all content of this directory to svn
    chdir(shortname)
    svn_operation(['add', '*']) 

    # 4. Commit
    svn_operation(['ci', '-m', 'problem ' + shortname + ' initial commit'])
    chdir('..')

