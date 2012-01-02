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
        result = True
        for f in (self.stdin_fh, self.stdout_fh, self.stderr_fh, self.process):
            if not f is None and not f.__exit__(type, value, traceback):
                result = False
        return result

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

    stdout = stderr = b''
    process = psutil.Popen(args, stdout = stdout_fh, stdin = stdin_fh,
                           stderr = stderr_fh, env = env, shell = shell)
    invoke_result = None
    with ExecutionControl(stdin_fh, stdout_fh, stderr_fh, process) as ec:
        invoke_result = invoker.invoke(process, limits)

        snapshot_after = snapshot.Snapshot()

        trash_remover.remove_trash(snapshot.get_changes(snapshot_before, snapshot_after), \
                           lang.is_compile_garbage)
        if nrout:
            stdout_fh.seek(0)
            stdout = stdout_fh.read();

        if nrerr:
            stderr_fh.seek(0)
            stderr = stderr_fh.read();


    return (invoke_result, stdout, stderr)
