from ..directory_diff import snapshot
from ..invoker import invoker
from ..language_configurator.lang_conf import get_language_configurator
import psutil
from subprocess import PIPE
from .. import globalconfig
from . import trash_remover
import threading
import logging
import random
import os

class RunnerError(Exception):
    pass

def __temp_file_name():
    name = 'tmp_' + str(random.randint(0, 1<<30))
    while os.path.exists(name):
        name = 'tmp_' + str(random.randint(0, 1<<30))
    return name    

def run(source, args_list = [], limits=globalconfig.default_limits, stdin_fh = None, \
        stdout_fh = None, stderr_fh = None, env=None, encoding = 'utf-8', shell = False):
    """
    Runs the binary, associated with language of the source given.
    Also removes al the trash, generated during running (Ex: *.pyc)
    Returns tuple of (invoker.ResultInfo, stdout, stderr)
    Parameters:
        source - path to the source, previously compiled
        args_list - list of additional argumets given to the binary
        limits - Executions limits, taken from globalconfig.py
        stdin_fh, stdout_fh, stderr_fh - File handlers, redirected to the launched binary
        env - a dict that defines the environment variables for the new process.
            For more info see "subprocess" in the python3 documentation

    Usage examples:
        run("a.cpp")
        run("C:\\New Folder\\a.cpp", ["1", "3"], invoker.ExecutionLimits(10, 256), \
            file_handler, env = {"PATH": "C:\\Python32"})
    """
    log = logging.getLogger("please_logger.executors.runner.run")
    snapshot_before = snapshot.Snapshot()
 
    tmp_stdout = None
    tmp_stderr = None
        
    if stdout_fh is None:
        tmp_stdout = __temp_file_name()
        log.debug('creating stdout_fh %s', tmp_stdout)
        stdout_fh = open(tmp_stdout, 'wb')
            
    if stderr_fh is None:
        tmp_stderr = __temp_file_name()
        log.debug('creating stderr_fh %s', tmp_stderr)
        stderr_fh = open(tmp_stderr, 'wb')
    
    lang = get_language_configurator(source)
    cmd = lang.get_run_command(source)
    args = cmd + args_list
    log.debug("Starting process: args:%s, stdout:%s, stdin:%s, stderr:%s, env:%s", str(args), str(stdout_fh), str(stdin_fh), str(stderr_fh), str(env))   
    while True:
        try:
            process = psutil.Popen(args, stdout = stdout_fh, stdin = stdin_fh, stderr = stderr_fh, env = env, shell = shell)
            break
        except psutil.error.NoSuchProcess:
            log.info("NoSuchProcess error, trying again...")
        except Exception as e:
            log.error("Unknown exception while starting the process: %s", str(e))
            break
            

    result = invoker.invoke(process, limits)
    #print('\n'.join([c for a,b,c in os.walk('.')][0]))
    snapshot_after = snapshot.Snapshot()
    #log.debug('snapshot after: \n%s', str(snapshot_before))
    log.debug("Removing trash created...")
    

    trash_remover.remove_trash(snapshot.get_changes(snapshot_before, snapshot_after), \
                               lang.is_compile_garbage)        
    if tmp_stdout is None:
        stdout = None
    else:
        with open(tmp_stdout, 'rb') as stdout_fh:
            stdout = stdout_fh.read()
            stdout_fh.close()
        if (not (tmp_stdout is None)):
            if (not os.path.exists(tmp_stdout)):
                log.error('Somebody deleted {0}, which was tmp_stdout for runner' % (tmp_stdout))
            else:
                while os.path.exists(tmp_stdout):
                    os.remove(tmp_stdout)
     
    if tmp_stderr is None:
        stderr = None
    else:
        with open(tmp_stderr, 'rb') as stderr_fh:
            stderr = stderr_fh.read()
            stderr_fh.close()
        if (not (tmp_stderr is None)):
            if (not os.path.exists(tmp_stderr)):
                log.error('Somebody deleted {0}, which was tmp_stdout for runner' % (tmp_stderr))
            else:  
                while os.path.exists(tmp_stderr):
                    os.remove(tmp_stderr)
        
    return (result, stdout, stderr)
