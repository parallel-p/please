import psutil
from ..directory_diff.snapshot import Snapshot
from ..invoker import invoker
from ..language_configurator.lang_conf import get_language_configurator
from subprocess import PIPE
from .. import globalconfig
from . import trash_remover
from ..log import logger

class ExecutionControl:
    def __init__(self, stdin_fh, stdout_fh, stderr_fh, process):
        self.stdin_fh = stdin_fh
        self.stdout_fh = stdout_fh
        self.stderr_fh = stderr_fh
        self.process = process

    def __enter__(self):
        for f in (self.stdin_fh, self.stdout_fh, self.stderr_fh, self.process):
            if f is not None and f is not PIPE:
                f.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        result = True
        for f in (self.stdin_fh, self.stdout_fh, self.stderr_fh, self.process):
            if f is not None and f is not PIPE and not f.__exit__(type, value, traceback):
                result = False
        return result

def run(source, args_list = [], limits=globalconfig.default_limits, stdin = None, \
        stdout = PIPE, stderr = PIPE, env=None, encoding = 'utf-8', shell = False):
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

    snapshot_before = Snapshot()

    lang = get_language_configurator(source)
    cmd = lang.get_run_command(source)
    args = cmd + args_list
    logger.debug("Starting process: args:%s, stdout:%s, stdin:%s, "
                 "stderr:%s, env:%s", str(args), str(stdout), str(stdin),
                 str(stderr), str(env))

    process = psutil.Popen(args, stdout=stdout, stdin=stdin, stderr = stderr,
                           env = env, shell = shell)
    invoke_result = None
    with ExecutionControl(stdin, stdout, stderr, process):
        invoke_result = invoker.invoke(process, limits)

        snapshot_after = Snapshot()

        trash_remover.remove_trash(snapshot_before.get_changes(snapshot_after), \
                           lang.is_compile_garbage)
        out, err = process.communicate()
        out = out or b''
        err = err or b''


    return (invoke_result, out, err)
