import os.path
from . import base
from .. import exceptions
from .. import locale
from .. import sandbox
from .. import config
from ..generator import generator

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

        if not fs.exists(config.config.generateFile()):
            log.error(locale.get("problem.generate-not-found"))

class Statement(Base):
    # TODO: allow parameters --ps and ---pdf
    # (will need to rework config.texCommands to separate)
    NAMES = ['statement', 'statements']
    
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
        
        log.info(locale.get('commands.statement.doing').format(
            self.problem_name) + "...")

        statements = self.statements()
        if statements is None:
            raise exceptions.MalformedProblemError(locale.get("problem.statements-not-found"))

        sb = sandbox.Sandbox("make_statements")
        sb.push(config.config.texPrologue())
        fl = config.config.texFiles()
        for file in fl:
            sb.push(file)
        
        log.info(locale.get('commands.statement.preparing-tex-file'))
        # TeX will not accept \ in the filenames, so we need to adjust them here
        stmtPath = os.path.dirname( statements.file() ).replace("\\","/") 
        stmtFile = os.path.basename( statements.file() )
        relPath = sb.relPath(self.context.directory).replace("\\","/")
        
        texCode = ("\\input{%s}\n" % os.path.basename(config.config.texPrologue(True)) +
                   "\\import{%s/}{%s}\n" % (relPath + "/" + stmtPath, stmtFile) + 
                   "\\end{document}\n" )
        texFile = "statements_full"
        sb.echoToFile(texFile + ".tex", texCode)
        
        log.info(locale.get('commands.statement.running-tex'))
        cmds = config.config.texCommands()
        for cmd in cmds:
            sb.exec(cmd, texFile)

        log.info(locale.get('commands.statement.moving-pdf'))
        outputdir = config.config.statementsReadyDir(); 
        fs.del_dir(outputdir)
        fs.mkdir(outputdir)
        
        sb.pop(texFile + ".pdf", outputdir)
        sb.pop(texFile + ".ps", outputdir)
        
        log.info(locale.get('commands.statement.doing').format(self.problem_name) +
                 ": " + locale.get('done') + "! " + 
                 locale.get('see-dir').format(outputdir)
          )

class Generate(Base):
    NAMES = ['generate', 'build']
    
    @classmethod
    def usage(cls):
        return locale.get('commands.generate.usage')
    
    @classmethod
    def description(cls):
        return locale.get('commands.generate.description')

    def __init__(self, context, args):
        super(Generate, self).__init__(context, args)

    def handle(self):
        if len(self.args):
            raise exceptions.UserInputError(
                locale.get('too-much-arguments'), self)
        
        log = self.context.log
        fs = self.context.file_system
        
        log.info(locale.get('commands.generate.doing').format(
            self.problem_name) + "...")
            
        log.info(locale.get('commands.generate.running-script').format(
                    config.config.generateFile()))
        outputDir = config.config.testsReadyDir()
        fs.del_dir(outputDir)
        fs.mkdir(outputDir)
        gena = generator.Generator(config.config.generateFile(), log,  locale,  
                                   config.config)
        gena.execute(outputDir)
        
        log.info(locale.get('commands.generate.doing').format(self.problem_name) +
                 ": " + locale.get('done') + "! " + 
                 locale.get('see-dir').format(outputDir)
          )
