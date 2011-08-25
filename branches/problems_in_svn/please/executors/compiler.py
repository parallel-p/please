from ..language_configurator.lang_conf import get_language_configurator
import logging
from ..invoker import invoker
from .. import globalconfig
from ..directory_diff import snapshot
from . import trash_remover
import psutil
import subprocess
import os

class CompileError(Exception):
    pass
        
def compile(path, limits=globalconfig.default_limits):
    '''
        Description: compile given source, if success, 
            returns tuple (RESULT_INFO, STDOUT, STDERR), else raises CompileError
    '''
    log = logging.getLogger("please_logger.executors.compiler.compile")
    
    cur_folder = os.path.split(path)[0]
    if cur_folder == "":
        cur_folder = "."
    old_folder_state = snapshot.Snapshot(cur_folder)
    configurator = get_language_configurator(path)
    if(configurator is None):
        raise CompileError("Couldn't detect source language for file " + path)
    #
    #search for already created binary
    expected_binary_full_path = configurator.get_binary_name(path)
    expected_binary = os.path.basename(expected_binary_full_path[0])
    if expected_binary != "":
        log.debug("Searching for binary: "+expected_binary)
        file_list=os.listdir(cur_folder)
        if expected_binary in file_list:
            log.debug("Found expected binary")
            source_file_modification_time = os.path.getmtime(path)
            log.debug("||Source file last modified:" + str(source_file_modification_time)+ " ||")
            expected_binary_modification_time = os.path.getmtime(expected_binary_full_path[0])
            log.debug("||Binary last modified:" + str(expected_binary_modification_time)+" ||")
            if (source_file_modification_time < expected_binary_modification_time):
                log.debug("We shouldn't recompile")
                #log.info("Found already compiled binary, shouldn't recompile")
                return (invoker.ResultInfo("OK", 0, 0, 0, 0) , "", "")   
            else:
                log.debug("Source file was modified, we should recompile")
    #
    command = configurator.get_compile_command(path)
    if(command == [""]):
        return (invoker.ResultInfo("OK", 0, 0, 0, 0) , "", "")
    log.debug("Compiling: path:%s, limits:%s", str(path), str(str(limits)))
    log.info("Compiling: path:%s",str(path))
    log.debug("Compiler.py: running " + str(command))
    try:
        handler = psutil.Popen(command, \
                               stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    except OSError:
        raise CompileError("There is no compiler for file '" + path + "'")
    result = invoker.invoke(handler, limits)
    stdout, stderr = handler.communicate()
    new_folder_state = snapshot.Snapshot(cur_folder)
    trash_remover.remove_trash(snapshot.get_changes(old_folder_state, new_folder_state), configurator.is_compile_garbage)
    if(result.verdict != "OK"):
        raise CompileError("Compilation failed with: " + result.verdict + \
                           "\nSTDOUT:\n" + stdout.decode() + \
                           "\nSTDERR:\n" + stderr.decode())
    else:
        return (result, stdout, stderr)
    
