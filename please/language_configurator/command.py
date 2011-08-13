import os
import os.path
class CommandConfigurator:
    def get_run_command(self, source):
        return ["{0}".format(source)]
    def is_compile_garbage (self, source) :
        return False
    def get_binary_name(self, source):
        return ["{0}".format(source)]

def get_command_configurator():
    return CommandConfigurator()