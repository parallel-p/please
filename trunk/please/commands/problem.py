from . import base
from .. import locale

class Base(base.Command):
    def __init__(self, context, args):
        super(Base, self).__init__(context, args)
        
        from please.properties.problem import Problem
        self.properties = Problem(self.context.file_system)

    def validator(self):
        validator = self.properties.validator()
        if validator is None:
            from please.searcher.validator import Validator
            validator_file = Validator(self.context.file_system).file()
            if validator_file is not None:
                from please.properties.validator import Validator
                validator = Validator(validator_file)

        return validator
    
    def checker(self):
        checker = self.properties.checker()
        if checker is None:
            from please.searcher.checker import Checker
            checker_file = Checker(self.context.file_system).file()
            if checker_file is not None:
                from please.properties.checker import Checker
                checker = Checker(checker_file)

        return checker

    def statements(self):
        statements = self.properties.statements()
        if statements is None:
            from please.searcher.statements import Statements
            statements_file = Statements(self.context.file_system).file()
            if statements_file is not None:
                from please.properties.statements import Statements
                statements = Statements(statements_file)

        return statements

class Inspect(Base):
    NAMES = ['inspect', 'lint']
    
    @classmethod
    def usage(cls):
        return locale.get('commands.inspect.usage')
    
    @classmethod
    def description(cls):
        return locale.get('commands.inspect.description')

    def __init__(self, context, args):
        super(Inspect, self).__init__(context, args)

    def handle(self):
        log = self.context.log
        log.info('Running check problem command.')

        fs = self.context.file_system

        validator = self.validator()
        if validator is not None:
            log.info(locale.get("problem.validator-found") % validator.file())
        else:
            log.warning(locale.get("problem.validator-not-found"))

        checker = self.checker()
        if checker is not None:
            log.info(locale.get("problem.checker-found") % checker.file())
        else:
            log.error(locale.get("problem.checker-not-found"))

        statements = self.statements()
        if statements is not None:
            log.info(locale.get("problem.statements-found") % statements.file())
        else:
            log.warning(locale.get("problem.statements-not-found"))

        from .. import config
        if not fs.exists(config.PLEASE_GENERATE_FILE):
            log.error(locale.get("problem.generate-not-found"))
