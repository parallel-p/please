from ..language_configurator.lang_conf import get_language_configurator
import logging
from ..invoker import invoker
from .. import globalconfig
from ..directory_diff import snapshot
from . import trash_remover
from ..utils import form_error_output
import psutil
import subprocess
import os

class CompileError(Exception):
    pass

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
            returns tuple (RESULT_INFO, STDOUT, STDERR), else raises CompileError
    '''
    log = logging.getLogger("please_logger.executors.compiler.compile")
    
    cur_folder = os.path.dirname(path)
    if cur_folder == "":
        cur_folder = "."
    old_folder_state = snapshot.Snapshot(cur_folder)
    configurator = get_language_configurator(path)
    if configurator is None:
        raise CompileError("Couldn't detect source language for file " + path)
    DO_NOTHING_RESULT = (invoker.ResultInfo("OK", 0, 0, 0, 0) , "", "")
    need_binaries = configurator.get_binary_name(path)
    if already_compiled(path, need_binaries):
        #log.info("File %s was already compiled" % path)
        return DO_NOTHING_RESULT

    command = configurator.get_compile_command(path)
    if command is None or command == [""]:
        return DO_NOTHING_RESULT
    log.info("Compiling %s",str(path))
    log.debug("Compiler.py: running %s with limits %s" % (command, limits))
    try:
        handler = psutil.Popen(command, \
                               stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    except OSError:
        raise CompileError("There is no compiler for file '%s'" % path)
    result = invoker.invoke(handler, limits)
    stdout, stderr = handler.communicate()
    new_folder_state = snapshot.Snapshot(cur_folder)
    trash_remover.remove_trash(snapshot.get_changes(old_folder_state, new_folder_state), configurator.is_compile_garbage)
    if(result.verdict != "OK"):
        raise CompileError(form_error_output.process_err_exit("Compilation %s failed with:" % path, result.verdict, \
                                                              result.return_code, stdout.decode(), stderr.decode()))
    else:
        return (result, stdout, stderr)
    
