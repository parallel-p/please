#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from os.path import exists

class Locale:
    ERROR_INTERNAL = 'internal error (%s)'
    UNKNOWN_COMMAND = 'unknown command: %s'
    UNKNOWN_OPTION = 'unknown option: %s'

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
    def __call__( self, message, level = INFO, end='\n' ):
        self.write("[please:%s] \x1b[1;%dm%s\x1b[0m" % (self.message[level], self.color[level], message), end=end)
        return Exception(level, message)
    def write( self, message, end='', color=None ):
        if color is not None:
            message = "\x1b[1;%dm%s\x1b[0m" % (self.color[color], message)
        print(message, end=end)
        sys.stdout.flush()

class Tests:
    tests_dir = "tests"
    def check(self):
        if not exists(Tests.test_dir):
            return "No '%s' directory" % Tests.test_dir

        return ""

class ProblemProperties:
    filename = "problem.properties"
    def __init__(self):
        if not exists(ProblemProperties.filename):
            raise Exception("No '%s' file" % ProblemProperties.filename)

        import configparser
        from io import StringIO
        self.__config = configparser.ConfigParser()
        self.__config.readfp(
            StringIO(
                "[default]\n" +
                str(open(ProblemProperties.filename).read())
            )
        )

    def get(self, param, default = None):
        args = ("default", param)
        if self.__config.has_option(*args):
            return self.__config.get(*args)
        else:
            return default

class Validator:
    source_dir = "source"
    
    def __init__(self, properties):
        self.__properties = properties

    def check(self):
        from os.path import exists, join
        if not exists(Validator.source_dir):
            return "No '%s' directory" % Validator.source_dir

        validator_file = self.__properties.get("validator")
        if validator_file is None:
            pass #artificial intellegence

        validator_file = join(Validator.source_dir, validator_file)

        if not exists(validator_file):
            return "No validator file: '%s'" % validator_file

        return ""

class Please:
    def __init__( self, log ):
        log.warning('Please use this tool only on your own risk!')
        log.warning('It is under development now.')
        self.log = log
    def action_fail( self ):
        raise self.log.error(Locale.ERROR_INTERNAL % 'fail')
    def action_verify( self ):
        # Куда-то сюда нужно запихнуть 
        properties = ProblemProperties()
        validator = Validator(properties)
        checks = [validator]
        for check in checks:
            outcome = check.check()
            if outcome != "":
                print("Error: " + outcome)
                exit(1)
            raise self.log.error(Locale.ERROR_INTERNAL % 'todo')
    def work( self, arguments ):
        command = []
        for s in arguments:
            if len(s) > 0 and s[0] != '-':
                command.append(s)
            elif len(s) > 1 and s[1] == '-':
                if s == '--recursive':
                    options.recursive = True
                else:
                    raise self.log.error(Locale.UNKNOWN_OPTION % s)
            else:
                raise self.log.error(Locale.UNKNOWN_OPTION % s)
        action = self.action_fail
        if len(command) == 0:
            action = self.action_verify
        else:
            return self.log.error(Locale.UNKNOWN_COMMAND % command[0])
        action()


log = Log()
please = Please(log)

if __name__ == '__main__':
    try:
        please.work(sys.argv[1:])
    except Exception as e:
        print(str(e))
        exit(1)


