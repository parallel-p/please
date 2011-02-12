from . import base
from .. import exceptions
from .. import locale

class Base(base.Command):
    def __init__(self, context, args):
        super(Base, self).__init__(context, args)
        
        from please.properties.problem import Problem
        self.properties = Problem(self.context.file_system)
        self.problem_name = self.context.file_system.root_basename()

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
        if len(self.args):
            raise exceptions.UserInputError(
                locale.get('too-much-arguments'), self)
        
        log = self.context.log
        fs = self.context.file_system
        
        log.info(locale.get('commands.inspect.header').format(
            self.problem_name))

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
        if not fs.exists(config.config.generateFile()):
            log.error(locale.get("problem.generate-not-found"))

class Statement(Base):
    NAMES = ['statement']
    
    @classmethod
    def usage(cls):
        return locale.get('commands.statement.usage')
    
    @classmethod
    def description(cls):
        return locale.get('commands.statement.description')

    def __init__(self, context, args):
        super(Statement, self).__init__(context, args)

    def handle(self):
        if len(self.args):
            raise exceptions.UserInputError(
                locale.get('too-much-arguments'), self)
        
        log = self.context.log
        fs = self.context.file_system
        
        log.info(locale.get('commands.statement.header').format(
            self.problem_name))

        statements = self.statements()
        if statements is None:
            raise exceptions.MalformedProblemError(locale.get("problem.statements-not-found"))
	  
        log.info(locale.get('commands.statement.preparing-tex-file'))
        
        from .. import config
        from os import path, chdir
                       
        workdir = path.join(config.config.pleaseDir(), "work"); # or should this be in config? --- PK
        fs.del_dir(workdir)
        fs.mkdir(workdir)
        
        chdir(workdir)
        
        texfile = "statement_full"
        stmtfile = statements.file().replace("\\","/") # TeX will not accept \ in the filename
        
        f = open(texfile + ".tex", "w");
        f.write("\\input{../../../_prologue.tex}\n"); # should be got from configuration, I think, and should have different path --- PK
        f.write("\\import{../../}{%s}\n" % stmtfile)
        f.write("\\end{document}\n");
        f.close()
        
        log.info(locale.get('commands.statement.running-tex'))
        
        # TeX commands should also come from configuration, I think --- PK
        fs.exec("latex", texfile + ".tex")
        fs.exec("latex", texfile + ".tex")
        fs.exec("dvips", texfile)
        fs.exec("dvipdfm", texfile)
       
        chdir("../..") # should use something like pushdir/popdir --- PK
        
        log.info(locale.get('commands.statement.moving-pdf'))
        
        outputdir = path.join(config.config.pleaseDir(), "statement-ready"); # or should this be in config? --- PK
        fs.del_dir(outputdir)
        fs.mkdir(outputdir)
        
        fs.copy(path.join(workdir, texfile + ".pdf"), path.join(outputdir, texfile + ".pdf"))
        fs.copy(path.join(workdir, texfile + ".ps"), path.join(outputdir, texfile + ".ps"))
        
        log.info(locale.get('done'))
       
