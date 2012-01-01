import os
import hashlib
from ..package.config import Config
from ..todo import painter

class TodoGenerator: 
    """ 
    this class prints todo list in please console
    
    red color - file does not exist
    yellow color - file is default
    green color - file had been modified by user
    
    you can use it as 
        please show todo <realative way>
    if you are not in the root of problem folder 
    or
        please show todo
    if you are in problem folder
    """
    def __init__(self, root_path='.'):
     
        md5path = os.path.join(root_path, '.please', 'md5.config')
        if os.path.exists(md5path):
            
            self.md5value = dict()
            with open(md5path) as md5file:
                for s in md5file:
                    resource, md5 = s.strip().split(':')
                    self.md5value[resource] = md5
    
    def get_todo(self, root_path = "."): 
        # prints todo        
        initial_position = os.getcwd()
        if (os.path.exists(root_path)):
            pass
        else:
            raise "problem does not exist"
        config_path = "default.package"
        with open(config_path) as config_file:
            config_text = "\n".join(config_file.readlines())
        self.__config = Config(config_text) 
        items = ["statement", "checker", "description", "analysis", "validator", "main_solution"]        
        for item in items:
            self.print_to_console(self.__get_item_status(item), item)
        tests_description_path = "tests.please"
        self.print_to_console(self.__get_item_status(path=tests_description_path, item="tests_description"), "tests description")
        
        if (root_path != "."):
            os.chdir(initial_position)
            
    def print_to_console(self, status, text):
        """ prints message to please console. color depends on objective's status"""
        if (status == "ok"):
            print(painter.ok(text + " ok"))
        elif (status == "warning"):
            print(painter.warning(text + " is default"))
        else:
            print(painter.error(text + " does not exist"))
    

    def __get_item_status(self, item=None, path = None):
        """
        Description:
        this function returns one of three item statuses (types):
        1) error - the file does not exist, or it's path is not written in config
        2) warning - the file exists, it's path is written in config file, or it's path is default,
        but the file is default(it's modification time is lower, than problem generation time)
        3) ok - the file exists, it's path is written in config file, or it's path is default,
        and this file is not default(it's modification time is greater, than problem generation time)
        """
        if (path != None):    
            item_path = path
        else:
            if (item in self.__config):
                item_path = self.__config[item]
            else:
                return("error")
        if (os.path.exists(item_path)):
            m = hashlib.md5()
            with open(item_path,"r+b") as item_file:
                m.update(item_file.read())
            if (m.hexdigest() != self.md5value[item]):
                return("ok")
            else:
                return("warning")
        else:
            return("error")
