#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os, re, shutil, subprocess, sys, threading, time

# t.py test tool — python clone of outdated t.cmd
# version 0.03-alpha0-r1  Every time you commit modified version of t.py, increment -r<number>
# copyright (c) Oleg Davydov, Yury Petrov
# This program is free sortware, under GPL, for great justice...

# t.py is being developed in a Subversion repository with t.sh:
# https://burunduk3.geins.ru/svn/public/t.sh
# You can get latest t.py version there. And, when you make changes to t.py,
# please commit it to this repository. Ask Oleg Davydov (burunduk3@gmail.com,
# vk.com/burunduk3) if you don't have access.

# === TODO LIST ===
#  0) restore t.sh features
#  1) help
#  2) external compilers configuration
#  3) problem.xml support
#  4) time & memory: invokation, limits, statistics
#  5) i18n support, simplified locale for windows
#  6) windows support — remove half of features if os is outdated

# === CHANGE LOG ===
#  2010-11-17 [burunduk3] work started



# === COMPILERS CONFIGURATION ==
# Здесь начинается конфигурация компиляторов. Мерзкая штука, не правда ли?

def compilers_configure():
  global configuration, suffixes
  def detector_python( source ):
    shabang = open(source, 'r').readline()
    if shabang[0:2] != '#!': shabang = ''
    if 'python3' in shabang: return 'python3'
    elif 'python2' in shabang: return 'python2'
    else: return 'python2' # python2 is default by now

  include_path = '../../../include'
  flags_c = ['-O2', '-Wall', '-Wextra', '-I', include_path, '-D__T_SH__', '-lm'] + os.environ['CFLAGS'].split(' ')
  flags_cpp = ['-O2', '-Wall', '-Wextra', '-I', include_path, '-D__T_SH__', '-lm'] + os.environ['CXXFLAGS'].split(' ')
  binary_default = lambda source: os.path.splitext(source)[0]
  binary_java = lambda source: os.path.splitext(source)[0] + '.class'
  binary_none = lambda source: source
  command_c = lambda source,binary: ['gcc'] + flags_c + ['-x', 'c', '-o', binary, source]
  command_cpp = lambda source,binary: ['g++'] + flags_cpp + ['-x', 'c++', '-o', binary, source]
  command_delphi = lambda source,binary: ['fpc', '-Mdelphi', '-O3', '-FE.', '-v0ewn', '-Sd', '-Fu' + include_path, '-Fi' + include_path, '-d__T_SH__', '-o'+binary, source]
  command_pascal = lambda source,binary: ['fpc', '-O3', '-FE.', '-v0ewn', '-Sd', '-Fu' + include_path, '-Fi' + include_path, '-d__T_SH__', '-o'+binary, source]
  executable_default = lambda binary: Executable(binary)
  executable_bash = lambda binary: Executable(binary, ['bash', binary])
  executable_java = lambda binary: Executable(binary, ['java', '-Xmx256M', '-Xss128M', '-ea', '-cp', os.path.dirname(binary), os.path.splitext(os.path.basename(binary))[0]], add=False)
  executable_perl = lambda binary: Executable(binary, ['perl', binary])
  executable_python2 = lambda binary: Executable(binary, ['python2', binary])
  executable_python3 = lambda binary: Executable(binary, ['python3', binary])

  configuration.detector = {
    'c': 'c', 'c++': 'c++', 'C': 'c++', 'cxx': 'c++', 'cpp': 'c++',
    'pas': 'pascal', 'dpr': 'delphi',
    'java': 'java', 'pl': 'perl', 'py': detector_python, 'sh': 'bash'
  }
  configuration.compilers = {
    'bash': Compiler(binary_none, None, executable_bash),
    'c': Compiler(binary_default, command_c, executable_default),
    'c++': Compiler(binary_default, command_cpp, executable_default),
    'delphi': Compiler(binary_default, command_delphi, executable_default),
    'java': Compiler(binary_java, lambda source,binary: ['javac', source], executable_java),
    'pascal': Compiler(binary_default, command_pascal, executable_default),
    'perl': Compiler(binary_none, None, executable_perl),
    'python2': Compiler(binary_none, None, executable_python2),
    'python3': Compiler(binary_none, None, executable_python3)
  }
  suffixes = configuration.detector.keys()



# === PARTS OF t.sh ===

## GCC flags
#gccVersionString=`gcc --version | head -n 1`
#gccVersion=${gccVersionString##* }
#gccVersionMajor=${gccVersion##*.}
#if [ $gccVersionMajor == "4" ] ; then
#  CFLAGS="-O2 -Wall -Wextra -I $INCLUDE_PATH -D__T_SH__"
#else
#  CFLAGS="-O2 -Wall -I $INCLUDE_PATH -D__T_SH__"
#fi
#CXXFLAGS="${CFLAGS}"
## End of GCC flags
#BINARY_SUFFIX=""
#if [ "$OPERATION_SYSTEM" != "Linux" ]; then
#  CFLAGS="$CFLAGS -Wl,--stack=134217728"
#  CXXFLAGS="$CXXFLAGS -Wl,--stack=134217728"
#  BINARY_SUFFIX=".exe"
#fi

class Log:
  DEBUG, INFO, NOTICE, WARNING, ERROR, FATAL = range(6)
  def __init__( self ):
    self.color = {Log.DEBUG: 37, Log.INFO: 36, Log.NOTICE: 32, Log.WARNING: 33, Log.ERROR: 31, Log.FATAL: 31}
    self.message = {Log.DEBUG: 'debug', Log.INFO: 'info', Log.NOTICE: 'notice', Log.WARNING: 'warning', Log.ERROR: 'error', Log.FATAL: 'fatal error'}
    self.debug = lambda text: self(text, Log.DEBUG)
    self.info = lambda text: self(text, Log.INFO)
    self.notice = lambda text: self(text, Log.NOTICE)
    self.warning = lambda text: self(text, Log.WARNING)
    self.error = lambda text: self(text, Log.ERROR)
    self.fatal = lambda text: self(text, Log.FATAL)
    pass
  def __call__( self, message, level = INFO, exit=None, end='\n' ):
    self.write("[t:%s] \x1b[1;%dm%s\x1b[0m" % (self.message[level], self.color[level], message), end=end)
    exit = exit if exit is not None else level >= Log.ERROR
    if exit: sys.exit(1)
  def write( self, message, end='', color=None ):
    if color is not None:
      message = "\x1b[1;%dm%s\x1b[0m" % (self.color[color], message)
    print(message, end=end)
    sys.stdout.flush()


class Configuration:
  def __init__( self ):
    self.compilers = {}
    self.detector = {}
  def detect_language( self, source ):
    global log
    suffix = os.path.splitext(source)[1][1:]
    if suffix not in self.detector: return None
    detector = self.detector[suffix]
    if type(detector) == str: return self.compilers[detector]
    return self.compilers[detector(source)]

class Compiler:
  def __init__( self, binary, command, executable ):
    self.binary, self.command, self.executable = binary, command, executable
  def __call__( self, source ):
    global log
    binary = self.binary(source)
    if binary == source or self.command is None or (os.path.isfile(binary) and os.stat(binary).st_mtime >= os.stat(source).st_mtime):
      log('compile skipped: %s' % binary)
    else:
      log('compile: %s → %s' % (source, binary))
      command = self.command(source, binary)
      process = subprocess.Popen(command)
      process.communicate()
      if process.returncode != 0: return None
    return self.executable(binary)


class Executable:
  def __init__( self, path, command=[], add=True ):
    directory, filename = os.path.split(path)
    directory = '.' if directory == '' else directory
    path = os.path.join(directory, filename)
    self.path, self.command = path, list(command)
    if add: self.command.append(self.path)
  def __str__( self ):
    return self.path
  def __call__( self, arguments=[], stdin=None, stdout=None, stderr=None ):
    process = subprocess.Popen(self.command + arguments, stdin=stdin, stdout=stdout, stderr=stderr)
    process.communicate()
    return process.returncode == 0

class RunResult:
  RUNTIME, TIME_LIMIT, MEMORY_LIMIT, OK = range(4)
  def __init__( self, result, exitcode, comment = '' ):
    self.result, self.exitcode, self.comment = result, exitcode, comment

class Invoker:
  def __init__( self, executable, limit_time, limit_memory ):
    self.executable, self.limit_time, self.limit_memory = executable, limit_time, limit_memory
  def waiter( self ):
    self.process.communicate()
    self.condition.acquire()
    self.condition.notify()
    self.condition.release()
  def run( self, stdin=None, stdout=None, stderr=None ):
    global log
    resource.setrlimit(resource.RLIMIT_CPU, (self.limit_time, -1))
    resource.setrlimit(resource.RLIMIT_DATA, (self.limit_memory, -1))
    start = time.time()
    self.process = subprocess.Popen(self.executable.command, stdin=stdin, stdout=stdout, stderr=stderr)
    pid = self.process.pid
    self.condition = threading.Condition()
    thread = threading.Thread(target=self.waiter)
    thread.start()
    force_result = None
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
        line = "%.3f" % (time.time() - start)
        line = line + '\b' * len(line)
        log.write(line)
        if mem_usage > self.limit_memory:
          force_result = RunResult(RunResult.MEMORY_LIMIT, -1, 'memory usage: %d' % mem_usage)
          self.process.terminate()
      except IOError:
        pass
    line = "[%.3f] " % (time.time() - start)
    log.write(line)
    if force_result is not None:
      return force_result
    code = self.process.returncode
    if code == -signal.SIGXCPU:
      return RunResult(RunResult.TIME_LIMIT, code, 'signal SIGXCPU received')
    elif code != 0:
      return RunResult(RunResult.RUNTIME, code, 'runtime error %d' % code)
    else:
      return RunResult(RunResult.OK, code)


def find_problems( base = '.' ):
  queue = [os.path.abspath(base)]
  for path in queue:
    if not os.path.isdir(path): continue;
    if os.path.exists(os.path.join(path, 'tests')) or os.path.exists(os.path.join(path, 'source')) or os.path.exists(os.path.join(path, 'src')):
      yield path
    else:
      queue += [os.path.join(path, x) for x in sorted(os.listdir(path))]

def find_source( path ):
  global suffixes
  for filename in [path + '.' + suffix for suffix in suffixes]:
    if os.path.isfile(filename):
      return filename
  if os.path.isfile(path):
    return path
  return None

def find_tests( path = '.' ):
  for filename in sorted(os.listdir(path)):
    if not re.match('^\d{2,3}$', filename): continue
    if not os.path.isfile(os.path.join(path, filename)): continue
    yield filename

def find_solution( path, token, problem ):
  result = find_source(os.path.join(path, token))
  if result is not None: return result
  result = find_source(os.path.join(path, problem + '_' + token))
  if result is not None: return result
  # В t.sh был ещё один случай: когда мы выбираем файл c именем <problem>_<token>, но не делаем find_source.
  # Я пока не буду это здесь повторять, потому что не могу придумать случай, когда это нужно.
  return None


def read_problem_properties( filename ):
  result = {}
  for line in open(filename, 'r').readlines():
    line = [token.strip() for token in line.split('=', 1)]
    if len(line) != 2: continue
    result[line[0]] = line[1]
  return result

def read_configuration( path ):
  problem_name = os.path.basename(os.path.abspath(path))
  configuration = {'path': path, 'name': problem_name}
  ppfile = os.path.join(path, 'problem.properties')
  if os.path.isfile(ppfile):
    configuration.update(read_problem_properties(ppfile))
  for name, value in [
    ('input-file', problem_name + '.in'),
    ('output-file', problem_name + '.out'),
    ('time-limit', 5),
    ('memory-limit', 256 * 2**20)
  ]:
    if name in configuration: continue
    configuration[name] = value
  for name in ['time-limit', 'memory-limit']:
    configuration[name] = int(configuration[name])
  for directory in ['source', 'src', 'tests']:
    if os.path.isdir(os.path.join(path, directory)):
      configuration.update({'source-directory': os.path.join(path, directory)})
      break
  configuration.update({'tests-directory': os.path.join(path, 'tests')})
  return configuration

def convert_tests( tests ):
  log('convert tests', end='')
  for test in tests:
    log.write('.')
    p = subprocess.Popen(['dos2unix', test], stderr=open('/dev/null', 'w'))
    p.communicate()
    if p.returncode != 0: log.warning('dos2unix failed on test %s' % test)
    if not os.path.isfile(test + '.a'):
      continue
    p = subprocess.Popen(['dos2unix', test + '.a'], stderr=open('/dev/null', 'w'))
    p.communicate()
    if p.returncode != 0: log.warning('dos2unix failed on file %s.a' % test)
  log.write('done\n')

def just_run( source, stdin=None, stdout=None ):
  global configuration, log
  compiler = configuration.detect_language(source)
  if compiler is None:
    log.warning("%s: cannot detect language" % source)
    return None
  executable = compiler(source)
  if executable is None:
    log.warning("%s: compilation error" % executable)
    return None
  return executable(stdin=stdin, stdout=stdout)

def build_problem( problem_configuration ):
  global configuration, log
  path = problem_configuration['path']
  problem_name = problem_configuration['name']
  log('== building problem “%s” ==' % problem_name)
  config_names = {'path': 'problem path', 'solution': 'default solution', 'source-directory': 'source directory', 'input-file': 'input file', 'output-file': 'output file'}
  for key in sorted(problem_configuration.keys()):
    name = config_names[key] if key in config_names else ('“%s”' % key)
    log('  * %s: %s' % (name, problem_configuration[key]))
  if 'solution' not in problem_configuration: log.warning('No solution defined for problem %s.' % problem_name)
  if 'source-directory' not in problem_configuration: log.error('No source directory defined for problem %s.' % problem_name)
  os.chdir(path)
  # cleanup
  if os.path.isdir(problem_configuration['tests-directory']):
    for filename in os.listdir(problem_configuration['tests-directory']):
      if re.match('^\d{2,3}(\.a)?$', filename):
        os.remove(os.path.join(problem_configuration['tests-directory'], filename))
  else:
    os.mkdir(problem_configuration['tests-directory'])
  #
  os.chdir(problem_configuration['source-directory'])
  doall = find_source('doall')
  if doall is not None:
    log('using generator: %s' % doall)
    result = just_run(doall)
    if not result: log.error('generator failed')
  else:
    log('auto-generating tests')
    count_hand, count_gen = 0, 0
    for test in ['%02d' % i for i in range(100)]:
      target = os.path.join(problem_configuration['tests-directory'], test)
      if os.path.isfile(test + '.hand'):
        shutil.copy(test + '.hand', target)
        count_hand += 1
      elif os.path.isfile(test + '.manual'):
        shutil.copy(test + '.manual', target)
        count_hand += 1
      else:
        generator = find_source('do' + test)
        generator = find_source('gen' + test) if generator is None else generator
        if generator is None: continue
        result = just_run(generator, stdout=open(target, 'w'))
        if not result: log.error('generator (%s) failed' % generator)
        count_gen += 1
    if count_hand != 0: log('manual tests copied: %d' % count_hand)
    if count_gen != 0: log('generated tests: %d' % count_gen)
  tests = list(find_tests(problem_configuration['tests-directory']))
  if not tests: log.error('no tests found in %s' % problem_configuration['tests-directory'])
  log('tests (total: %d): %s' % (len(tests), ','.join(tests)))
  os.chdir(problem_configuration['tests-directory'])
  convert_tests(tests)
  validator = None
  for name in ['validate', 'validator']:
    validator = find_source(os.path.join(problem_configuration['source-directory'], name))
    if validator is not None: break
  if validator is not None:
    compiler = configuration.detect_language(validator)
    validator = compiler(validator)
    log('validate tests', end='')
    for test in tests:
      log.write('.')
      if validator(arguments=[test], stdin=open(test, 'r')): continue
      log.error('Test %s failed validation.' % test)
    log.write('done\n')
  solution = find_solution(path, problem_configuration['solution'], problem_name) if 'solution' in problem_configuration else None
  if solution is None:
    log.warning('Solution not found.')
    return False
  solution = os.path.join(path, solution)
  compiler = configuration.detect_language(solution)
  solution = compiler(solution)
  log('generate answers', end='')
  input_name, output_name = problem_configuration['input-file'], problem_configuration['output-file']
  input_name = problem_name + '.in' if input_name == '<stdin>' else input_name
  output_name = problem_name + '.out' if output_name == '<stdout>' else output_name
  for test in tests:
    if os.path.isfile(test + '.a'):
      log.write('+')
      continue
    log.write('.')
    shutil.copy(test, input_name)
    r = solution(
      stdin=open(input_name, 'r') if problem_configuration['input-file'] == '<stdin>' else None,
      stdout=open(output_name, 'w') if problem_configuration['output-file'] == '<stdout>' else None)
    if not r: log.error('Solution failed on test %s.' % test)
    shutil.copy(output_name, test + '.a')
  log.write('done\n')
  return True


def check_problem( problem_configuration, solution=None ):
  global configuration, log
  problem_name = problem_configuration['name']
  os.chdir(problem_configuration['tests-directory'])
  tests = list(find_tests(problem_configuration['tests-directory']))
  if not tests:
    log.warning('No tests found for problem %s.' % problem_name)
    return False
  checker = None
  for checker_name in ['check', 'checker', 'check_' + problem_name, 'checker_' + problem_name]:
    checker = find_source(os.path.join('..', checker_name))
    if checker is not None: break
  if checker is None:
    log.warning('Checker wasn\'t found, solution wouldn\'t be checked.')
    return False
  compiler = configuration.detect_language(checker)
  checker = compiler(checker)
  if checker is None:
    log.warning('Checker: compilation error.')
    return False
  solution_name = problem_configuration['solution'] if solution is None else solution
  solution = find_solution(problem_configuration['path'], solution_name, problem_name)
  if solution is None:
    log.warning('Solution (%s) wasn\'t found.' % solution_name)
    return False
  compiler = configuration.detect_language(solution)
  solution = compiler(solution)
  if solution is None:
    log.warning('Solution (%s): compilation error.' % solution_name)
    return False
  log.info('checking solution: %s' % solution)
  input_name, output_name = problem_configuration['input-file'], problem_configuration['output-file']
  input_name = problem_name + '.in' if input_name == '<stdin>' else input_name
  output_name = problem_name + '.out' if output_name == '<stdout>' else output_name
  invoker = Invoker(solution, problem_configuration['time-limit'], problem_configuration['memory-limit'])
  for test in tests:
    log('test [%s] ' % test, Log.INFO, end='')
    shutil.copy(test, input_name)
    r = invoker.run(
      stdin=open(input_name, 'r') if problem_configuration['input-file'] == '<stdin>' else None,
      stdout=open(output_name, 'w') if problem_configuration['output-file'] == '<stdout>' else None)
    good = False
    if r.result == RunResult.RUNTIME:
      log.write('Runtime error (%s).' % r.comment, end='\n', color=Log.ERROR)
    elif r.result == RunResult.TIME_LIMIT:
      log.write('Time limit exceeded (%s).' % r.comment, end='\n', color=Log.ERROR)
    elif r.result == RunResult.MEMORY_LIMIT:
      log.write('Memory limit exceeded (%s)' % r.comment, end='\n', color=Log.ERROR)
    elif r.result == RunResult.OK:
      good = True
    else:
      log.fatal('Invokation failed (%s).' % r.comment)
    if not good:
      return False
    log.write('* ')
    result = checker(arguments=[input_name, output_name, test + '.a'])
    if not result: log.error('Wrong answer on test %s.' % test)
  return True

def clean_problem( path ):
  global log, suffixes, options
  os.chdir(path)
  remove_tests = 'no-remove-tests' not in options or not options['no-remove-tests']
  if remove_tests and os.path.isdir('tests'):
    for filename in os.listdir('tests'):
      if not re.match('^\d{2,3}(.a)?$', filename): continue
      os.remove(os.path.join('tests', filename))
  if os.path.isfile(os.path.join('tests', 'tests.gen')): os.remove(os.path.join('tests', 'tests.gen'))
  for directory in [os.path.join(path, sub) for sub in ['.', 'tests', 'src', 'source']]:
    if not os.path.isdir(directory): continue
    for filename in os.listdir(directory):
      if re.search('\.(in|out|log|exe|dcu|ppu|o|obj|class|hi|manifest|pyc|pyo)$', filename):
        os.remove(os.path.join(directory, filename))
      for suffix in suffixes:
        if not os.path.isfile(os.path.join(directory, filename + '.' + suffix)): continue
        os.remove(os.path.join(directory, filename))
        break
    if remove_tests:
      os.chdir(directory)
      cleaner_name = find_source('wipe')
      if cleaner_name is None: continue
      result = just_run(cleaner_name)
      if not result:
        log.warning('%s returned non-zero' % cleaner)
  os.chdir(path)
  if remove_tests and (os.path.isdir('source') or os.path.isdir('src')) and os.path.isdir('tests'):
    os.rmdir('tests')

def prepare():
  import resource as r, signal as s
  global resource, signal
  resource, signal = r, s
  resource.setrlimit(resource.RLIMIT_STACK, (-1, -1)) # 

def prepare_windows():
  # Это выглядит как мерзкий, грязный хак, каковым является вообще любая работа с windows.
  import ctypes

  STD_INPUT_HANDLE = -10
  STD_OUTPUT_HANDLE= -11
  STD_ERROR_HANDLE = -12

  FOREGROUND_BLUE = 0x01
  FOREGROUND_GREEN= 0x02
  FOREGROUND_RED  = 0x04
  FOREGROUND_INTENSITY = 0x08
  BACKGROUND_BLUE = 0x10
  BACKGROUND_GREEN= 0x20
  BACKGROUND_RED  = 0x40
  BACKGROUND_INTENSITY = 0x80
  windows_colors = [
    0, # black
    FOREGROUND_RED, # red
    FOREGROUND_GREEN, #green
    FOREGROUND_GREEN|FOREGROUND_RED, # brown
    FOREGROUND_BLUE, # blue
    FOREGROUND_BLUE|FOREGROUND_RED, # magenta
    FOREGROUND_BLUE|FOREGROUND_GREEN, # skyblue
    FOREGROUND_BLUE|FOREGROUND_GREEN|FOREGROUND_RED, # gray
    0,0,0
  ]
  def windows_write( text, end='' ):
    text += end
    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    pieces = text.split('\x1b[')
    sys.stdout.write(pieces[0])
    sys.stdout.flush()
    for str in pieces[1:]:
      color, line = str.split('m', 1)
      numbers = [int(x) for x in color.split(';')]
      mask = 0
      for x in numbers:
        if x == 0: mask |= windows_colors[7]
        if x == 1: mask |= FOREGROUND_INTENSITY
        if 30 <= x <= 39: mask |= windows_colors[x - 30]
      ctypes.windll.kernel32.SetConsoleTextAttribute(handle, mask)
      sys.stdout.write(line.encode('utf8').decode('ibm866'))
      sys.stdout.flush()
  def windows_convert_tests( tests ):
    pass
  log.write = windows_write
  convert_tests = windows_convert_tests

def arguments_parse():
  arguments, arguments_force = [], False
  options = {
    'no-remove-tests': False,
    'recursive': False
  }
  for arg in sys.argv[1:]:
    if len(arg) >= 1 and arg[0] == '-' and not arguments_force:
      if len(arg) >= 2 and arg[1] == '-':
        if arg == '--': arguments_force = True
        elif arg == '--no-remove-tests': options['no-remove-tests'] = True
        elif arg == '--recursive': options['recursive'] = True
        else:
          pass
      else:
        for option in arg[1:]:
          if option == 't': options['no-remove-tests'] = True
          elif option == 'r': options['recursive'] = True
          else:
            pass
    else:
      arguments.append(arg)
  return options, arguments
  

if sys.platform == 'win32': # if os is outdated
  prepare = prepare_windows

log = Log()
log.warning('You are using testing branch of t.sh, that is under heavy development how.')
configuration = Configuration()
compilers_configure()
prepare()

options, arguments = arguments_parse()

command = arguments[0] if len(arguments) > 0 else None
problems = find_problems() if options['recursive'] else [os.path.abspath('.')]

for problem in problems:
  problem_configuration = read_configuration(problem)
  if command == 'build':
    build_problem(problem_configuration)
    check_problem(problem_configuration)
  elif command == 'check':
    if len(arguments) > 1:
      problem_configuration['solution'] = arguments[1]
    check_problem(problem_configuration)
  elif command == 'clean':
    clean_problem(problem)

