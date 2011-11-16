from ..directory_diff import snapshot
from ..invoker import invoker
from ..language_configurator.lang_conf import get_language_configurator
import psutil
import tempfile
from subprocess import PIPE
from .. import globalconfig
from . import trash_remover
import threading
from please.log import logger
import random
import os

class RunnerError(Exception):
    pass

def __temp_file_name():
    name = 'tmp_' + str(random.randint(0, 1<<30))
    while os.path.exists(name):
        name = 'tmp_' + str(random.randint(0, 1<<30))
    return name

class ExecutionControl:
    def __init__(self, stdin_fh, stdout_fh, stderr_fh, process):
        self.stdin_fh = stdin_fh
        self.stdout_fh = stdout_fh
        self.stderr_fh = stderr_fh
        self.process = process

    def __enter__(self):
        for f in (self.stdin_fh, self.stdout_fh, self.stderr_fh, self.process):
            if (not f is None):
                f.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        b = True
        for f in (self.stdin_fh, self.stdout_fh, self.stderr_fh, self.process):
            if not f is None:
                b = b or (f.__exit__(type, value, traceback) == True)
        if (isinstance(type, psutil.error.NoSuchProcess)):
            b = True
        return b

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

    snapshot_before = snapshot.Snapshot()

    nrout = False;
    nrerr = False;

    if stdout_fh is None:
        nrout = True
        stdout_fh = tempfile.TemporaryFile()

    if stderr_fh is None:
        nrerr = True
        stderr_fh = tempfile.TemporaryFile()

    lang = get_language_configurator(source)
    cmd = lang.get_run_command(source)
    args = cmd + args_list
    logger.debug("Starting process: args:%s, stdout:%s, stdin:%s, stderr:%s, env:%s", str(args), str(stdout_fh), str(stdin_fh), str(stderr_fh), str(env))

    stdout = stderr = ''
    process = psutil.Popen(args, stdout = stdout_fh, stdin = stdin_fh, stderr = stderr_fh, env = env, shell = shell)
    result = None
    try:
        with ExecutionControl(stdin_fh, stdout_fh, stderr_fh, process) as ec:
            result = invoker.invoke(process, limits)

            snapshot_after = snapshot.Snapshot()

            trash_remover.remove_trash(snapshot.get_changes(snapshot_before, snapshot_after), \
                               lang.is_compile_garbage)
            if nrout:
                stdout_fh.seek(0)
                stdout = stdout_fh.read();

            if nrerr:
                stderr_fh.seek(0)
                stderr = stderr_fh.read();

    except psutil.error.NoSuchProcess:
        logger.error("NoSuchProcess error")
    #except Exception as e:
    #    logger.error("Unknown exception while invoking the process: %s", str(e))

    #print('\n'.join([c for a,b,c in os.walk('.')][0]))


    return (result, stdout, stderr)
