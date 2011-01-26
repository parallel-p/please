import subprocess, threading, time
import resource, signal

class RunResult:
  RUNTIME, TIME_LIMIT, MEMORY_LIMIT, OK = range(4)
  def __init__( self, result, exitcode, timepeak, memorypeak, comment = '' ):
    self.result, self.exitcode, self.timepeak, self.memorypeak, self.comment = result, exitcode, timepeak, memorypeak, comment

class Invoker:
  def __init__( self, limit_time = None, limit_idle = None, limit_memory = None, callback = None ):
    # limit_time — ограничение на процессорное время, использованное программой. Вещественное, задаётся в секундах.
    # limit_idle — ограничение на астрономическое время работы программы. Вещественное, задаётся в секундах.
    # limit_memory — ограничение на используемую память. Целое, задаётся в байтах.
    # None в любом из ограничений означает отсутствие явного ограничения.
    # callback — функция для получения статуса запущеной программы
    # TODO: известные проблемы:
    #   как обычно, с Java. Виртуальная машина сразу выделяет всё указанную память. При этом я не знаю способа
    #   средствами Java ограничить суммарную (стек+куча) память программы. А в Invoker, видимо, придётся передавать None.
    self.limit_time, self.limit_idle, self.limit_memory, self.callback = limit_time, limit_idle, limit_memory, callback
  def waiter( self ):
    self.process.communicate()
    # вообще получить бы более низкий уровень, чем то, что предоставляет subprocess
    # как вариант — вообще написать invoker на C и подключать модулем
    self.condition.acquire()
    self.condition.notify()
    self.condition.release()
  def __call__( self, executable, stdin=None, stdout=None, stderr=None ):
    # executable — команда, которую нужно выполнить для запуска программы.
    # подробнее см. мануал по subprocess.Popen — четвёрка (executable, stdin, stdout, stderr)
    # передаётся туда без изменений.
    # TODO: сделать так, чтобы RLIMIT_CPU устанавливалось только на дочерний процесс,
    # и разобраться с RLIMIT_DATA — кажется, оно означает не совсем то, что нужно.
    # Ещё сделать, чтобы limit_time мог быть вещественным.
    resource.setrlimit(resource.RLIMIT_CPU, (self.limit_time if self.limit_time is not None else -1, -1))
    resource.setrlimit(resource.RLIMIT_DATA, (self.limit_memory if self.limit_memory is not None else -1, -1))
    start = time.time()
    self.process = subprocess.Popen(executable, stdin=stdin, stdout=stdout, stderr=stderr)
    pid = self.process.pid
    self.condition = threading.Condition()
    thread = threading.Thread(target=self.waiter)
    force_result = None
    memory_peak, time_peak = 0, 0
    thread.start()
    while True:
      self.condition.acquire()
      self.condition.wait(0.01)
      self.condition.release()
      if self.process.returncode is not None:
        break
      try: # так может случится, что процесс завершится в самый интересный момент
        stat = open("/proc/%d/stat" % pid, 'r')
        stats = stat.readline().split()
        stat.close()
        stat = open("/proc/%d/statm" % pid, 'r')
        stats_m = stat.readline().split()
        stat.close()
        cpu_time = (int(stats[13]) + int(stats[14])) # это ещё надо умножить на коэффициент, который хрен где получишь
        mem_usage = int(stats_m[0]) * 1024
        real_time = time.time() - start
        memory_peak = max(memory_peak, mem_usage)
        time_peak = max(time_peak, real_time)
        line = "%.3f" % real_time
        line = line + '\b' * len(line)
        if self.callback is not None: self.callback(line)
        if self.limit_idle is not None and real_time > self.limit_idle:
          force_result = RunResult(RunResult.IDLE_LIMIT, None, time_peak, memory_peak, 'time consumed: %.3f' % real_time)
          self.process.terminate()
        if self.limit_memory is not None and mem_usage > self.limit_memory:
          force_result = RunResult(RunResult.MEMORY_LIMIT, None, time_peak, memory_peak, 'memory usage: %d' % mem_usage)
          self.process.terminate()
      except IOError:
        pass
    line = "[%.3f] " % (time.time() - start) # Это астрономической время =(
    if self.callback is not None: self.callback(line)
    if force_result is not None:
      return force_result
    code = self.process.returncode
    if code == -signal.SIGXCPU:
      return RunResult(RunResult.TIME_LIMIT, code, time_peak, memory_peak, 'signal SIGXCPU received')
    elif code != 0:
      return RunResult(RunResult.RUNTIME, code, time_peak, memory_peak, 'runtime error %d' % code)
    else:
      return RunResult(RunResult.OK, code, time_peak, memory_peak)

