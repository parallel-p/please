import psutil
import time
from ..utils import platform_detector

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
def invoke(handler, limits):
    CHECK_PERIOD = 0.05
    MEGABYTE = 1 << 20
    
    used_memory = 0
    cpu_time = 0
    verdict = None
    
    start_time = time.time()
    real_time = 0
    pid = handler.pid
    return_code = None 
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
        except psutil.error.NoSuchProcess as e:
            logger.warning("Couldn't check limits: NoSuchProcess")
            continue#sometimes it happens for unknown reasons
        except psutil.error.AccessDenied as e:
            try:#wait some time, in darwin process is steel running, but already not exists
                return_code = handler.wait(CHECK_PERIOD)
            except psutil.TimeoutExpired:
                pass
            logger.warning("Couldn't check limits: AccessDenied")
            continue#sometimes it happens for unknown reasons

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

    
    real_time = time.time() - start_time
    if real_time > limits.real_time:
        verdict = "real TL"
        return_code = None

    verdict = verdict or ("OK" if return_code == 0 else "RE")
    return ResultInfo(verdict, return_code, real_time, cpu_time, used_memory / MEGABYTE)

__current_platform = platform_detector.get_platform()

def __get_memory_info(handler):
    return handler.get_memory_info()[0]        
