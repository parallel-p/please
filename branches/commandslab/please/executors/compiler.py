from ..lang_config import get_lang_config
from ..lang_config.utils import is_windows
import tempfile
import logging
from ..invoker import invoker
from .. import globalconfig
from ..directory_diff.snapshot import Snapshot
from . import trash_remover
from ..utils import form_error_output
from ..utils.exceptions import PleaseException
import psutil
import subprocess
from subprocess import PIPE
import os

def already_compiled(src, need_binaries):
    for binary in need_binaries:
        if not os.path.exists(binary):
            return False
        source_file_modification_time = os.path.getmtime(src)
        expected_binary_modification_time = os.path.getmtime(binary)
        if source_file_modification_time >= expected_binary_modification_time:
            return False

    return True

def compile(path, limits=globalconfig.default_limits):
    '''
        Description: compile given source, if success, 
                     returns tuple (RESULT_INFO, STDOUT, STDERR)
    '''
    log = logging.getLogger("please_logger.executors.compiler.compile")
    
    cur_folder = os.path.dirname(path)
    if cur_folder == "":
        cur_folder = "."
    old_folder_state = Snapshot(cur_folder)
    config = get_lang_config(path)
    if config is None:
        raise PleaseException("Can't detect source language for file " + path)
    DO_NOTHING_RESULT = (invoker.ResultInfo("OK", 0, 0, 0, 0) , "", "")
    need_binaries = config.binaries
    if already_compiled(path, need_binaries):
        #log.info("File %s was already compiled" % path)
        return DO_NOTHING_RESULT

    commands = config.compile_commands
    log.info("Compiling %s",str(path))
    stdout, stderr = [], []
    error = None
    env = dict(os.environ)
    env.update(config.environment)
    
    if not commands:
        result, out, err = DO_NOTHING_RESULT
        stdout.append(out)
        stderr.append(err)

    for command in commands:
        log.debug("Compiler.py: running %s with limits %s" % (command, limits))
        try:
            result, out, err = invoker.run_command(command, limits,
                                                   env = env)
        except OSError:
            error = PleaseException("There is no compiler for file '%s'" % path)
            break
        stdout.append(out)
        stderr.append(err)
        log.info("Compilation {0} succeded.".format(path) + form_error_output.form_err_string_by_std(out, err))
        if result.verdict != 'OK':
            error = PleaseException(form_error_output.process_err_exit(
                "Compilation %s failed with:" % path, result.verdict, \
                result.return_code, out, err))
            break
    new_folder_state = Snapshot(cur_folder)
    trash_remover.remove_trash(old_folder_state.get_changes(new_folder_state), config.is_compile_garbage)
    if error is not None:
        raise error
    else:
        return (result, stdout, stderr)
