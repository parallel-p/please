import os.path
class ExeConfigurator:
    def get_run_command(self, source):
        return "{0}".format(source)
    def is_compile_garbage (self, source) :
        return False

def get_exe_configurator():
    return ExeConfigurator()
