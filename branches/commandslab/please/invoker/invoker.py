import psutil
import time
from ..utils import platform_detector
import sys
import errno
import os
from subprocess import PIPE
import tempfile

_on_windows = sys.platform.startswith('win')

CHUNKSIZE = 4096

if _on_windows:
    import threading
    def _read(file, list, event):
        if file is None:
            return
        while True:
            bs = file.read(CHUNKSIZE)
            if not bs:
                break
            list.append(bs)
            if event.isSet():
                break
    def _new_reading_thread(file, list):
        event = threading.Event()
        thread = threading.Thread(target=_read, args=(file, list, event))
        thread.start()
        return thread, event
else:
    import fcntl
    import select
    _use_poll = hasattr(select, 'poll')

import logging
logger = logging.getLogger("please_logger.invoker")

class ResultInfo:
    '''
    This class represents all the information we have to get from the execution:
    * verdict: 
        possible values are:
          OK (program executed succesfully);
          TL (CPU time limit exceeded);
          real TL (real time limit exceeded)
          ML (memory limit exceeded);
          RE (program has returned non-zero code).
    * cpu time:
        cpu time in seconds, used by the program
    * real time:
        time in seconds, passed since the call of this method
    * used memory:
        memory in megabytes, used by the program
    * return code:
        code returned by the program
    '''
    def __init__(self, verdict, return_code, real_time, cpu_time, used_memory):
        self.verdict = verdict
        self.return_code = return_code
        self.real_time = real_time
        self.cpu_time = cpu_time
        self.used_memory = used_memory

    def __str__(self):
        return ("verdict: {0}\n" \
                + "return code: {1}\n" \
                + "real time: {2:.2f} sec, cpu time: {3:.2f} sec\n" \
                + "used memory: {4:.3f} Mb").format(self.verdict, self.return_code, 
                                                    self.real_time, self.cpu_time, 
                                                    self.used_memory)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (self.verdict == other.verdict and
                self.return_code == other.return_code and
                self.real_time == other.real_time and
                self.cpu_time == other.cpu_time and
                self.used_memory == other.used_memory)

class ExecutionLimits:
    '''
    This class represents constraints of the execution.
    '''
    def __init__(self, cpu_time=10, memory=512, real_time=None):
        real_time = real_time or cpu_time * 5
        self.real_time, self.memory, self.cpu_time = \
            real_time, memory, cpu_time 
        self.real_time = float(self.real_time)
        self.memory = float(self.memory)
        self.cpu_time = float(self.cpu_time)

    def __str__(self):
        return "cpu_time=%s, memory=%sMb, real_time=%s" % (
                self.cpu_time, self.memory, self.real_time)

    def __repr__(self):
        return self.__str__()

'''
This function controls the execution of the program.
It looks after memory limit, time limit (cpu and real),
that means that program will be terminated if it exeeds any of constraints.

It returns ResultInfo, showing result of execution.

Example of using:
  import psutil
  from subprocess import PIPE

  handler = psutil.Popen(["program.exe", "--arg1=first", "/arg2=second"],
                         stdout = PIPE) # read help(psutil.Popen)
  limits = ExecutionLimits(real_time=3, memory=128, cpu_time=10) 
                           # cpu_time can be omitted; by default it equals
                           # to real_time.
                           # Warning: don't use this value if you don't
                           # know what is it 

  result = invoke(handler, limits)
  print(str(result))
  if (result.verdict != "OK"):
      print("42")
  else:
      raise Exception(":-(")
'''

def run_command(args, limits, stdin = None, stdout = PIPE, stderr = PIPE, **kw):
    stdout_fh = stdout if stdout != PIPE else tempfile.TemporaryFile()
    stderr_fh = stderr if stderr != PIPE else tempfile.TemporaryFile()

    if stdin is None:
        stdin = open(os.devnull, 'rb')

    handler = psutil.Popen(args, stdin=stdin, stdout=stdout_fh, stderr=stderr_fh, **kw)
    res, retstdout, retstderr = invoke(handler, limits)
    if stdout == PIPE:
        stdout_fh.seek(0)
        retstdout = stdout_fh.read()
        stdout_fh.close()
    if stderr == PIPE:
        stderr_fh.seek(0)
        retstderr = stderr_fh.read()
        stderr_fh.close()

    return res, retstdout, retstderr

def invoke(handler, limits):
    CHECK_PERIOD = 0.05
    MEGABYTE = 1 << 20
    
    used_memory = 0
    cpu_time = 0
    verdict = None
    
    start_time = time.time()
    real_time = 0
    return_code = None 
    stdout = []
    stderr = []
    if _on_windows:
        outthread, outstop = _new_reading_thread(handler.stdout, stdout)
        errthread, errstop = _new_reading_thread(handler.stderr, stderr)
    elif _use_poll:
        poller = select.poll()
        flags = select.POLLIN | select.POLLPRI
        fds = {}
        outs = {}
        def _register(f, out):
            if f is not None:
                poller.register(f.fileno(), flags)
                fds[f.fileno()] = f
                outs[f.fileno()] = out
                fcntl.fcntl(f.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        _register(handler.stdout, stdout)
        _register(handler.stderr, stderr)
    else:
        write_set = [f for f in (handler.stdout, handler.stderr) if f is not None]
        for f in write_set:
            fcntl.fcntl(f.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
    while return_code is None:
        #wait some time before checking process information,
        #because in darwin it is access denied raised in first moment
        try:
            return_code = handler.wait(CHECK_PERIOD)
        except psutil.TimeoutExpired:
            pass
    
        try:
            cpu_time = sum(list(handler.get_cpu_times()))
            real_time = time.time() - start_time
            used_memory = max(used_memory, __get_memory_info(handler))
        except psutil.error.NoSuchProcess:
            #logger.warning("Couldn't check limits: NoSuchProcess")
            continue #sometimes it happens for unknown reasons
        except psutil.error.AccessDenied:
            try: #wait some time, in darwin process is steel running, but already not exists
                return_code = handler.wait(CHECK_PERIOD)
            except psutil.TimeoutExpired:
                pass
            #logger.warning("Couldn't check limits: AccessDenied")
            continue #sometimes it happens for unknown reasons

        if real_time > limits.real_time:
            handler.kill()
            verdict = "real TL"
            return_code = None
            break
        elif cpu_time > limits.cpu_time:
            handler.kill()
            verdict = "TL"
            return_code = None
            break
        elif used_memory > MEGABYTE * limits.memory:
            handler.kill()
            verdict = "ML"
            return_code = None
            break

        # Reading fun!
        if not _on_windows:
            if _use_poll:
                if not fds:
                    continue
                try:
                    events = poller.poll(0)
                except OSError as e:
                    if e.args[0] == errno.EINTR: # rewrite this for python 3.3
                        continue
                    raise
                for fd, mode in events:
                    if mode & flags: # actual message
                        try:
                            data = os.read(fd, CHUNKSIZE)
                        except OSError as e:
                            if e.args[0] == errno.EAGAIN:
                                continue
                            raise
                        if not data:
                            poller.unregister(fd)
                            del fds[fd]
                        outs[fd].append(data)
                    else:
                        poller.unregister(fd)
                        del fds[fd]
            else:
                rlist, wlist, xlist = select.select([], write_set, [], 0)
                if handler.stdout in wlist:
                    try:
                        data = handler.stdout.read(CHUNKSIZE)
                    except OSError as e:
                        if e.args[0] != errno.EAGAIN:
                            raise
                    else:
                        stdout.append(data)
                if handler.stderr in wlist:
                    try:
                        data = handler.stderr.read(CHUNKSIZE)
                    except OSError as e:
                        if e.args[0] != errno.EAGAIN:
                            raise
                    else:
                        stderr.append(data)

    if _on_windows:
        outstop.set()
        errstop.set()

    real_time = time.time() - start_time
    if real_time > limits.real_time:
        verdict = "real TL"
        return_code = None

    if handler.stdout is not None:
        try:
            stdout.append(handler.stdout.read())
        except (OSError, IOError):
            pass

    if handler.stderr is not None:
        try:
            stderr.append(handler.stderr.read())
        except (OSError, IOError):
            pass

    verdict = verdict or ("OK" if return_code == 0 else "RE")
    return (ResultInfo(verdict, return_code, real_time, cpu_time, used_memory / MEGABYTE),
            b''.join(stdout), b''.join(stderr))

__current_platform = platform_detector.get_platform()

def __get_memory_info(handler):
    return handler.get_memory_info()[0]        
