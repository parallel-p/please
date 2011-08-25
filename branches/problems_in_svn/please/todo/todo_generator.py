import os
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
    
    def get_todo(self, root_path = "."): 
        # prints todo        
        
        initial_position = os.getcwd()
        if (os.path.exists(root_path)):
            os.chdir(root_path) 
            time_file_path = os.path.join(".please", "time.config")
            time_file = open(time_file_path, "r")
            self.__folder_generation_time_sec = float(time_file.read())
            time_file.close()
        else:
            raise "problem does not exist"
        config_path = "default.package"
        config_file = open(config_path)
        config_text = "\n".join(config_file.readlines())
        self.__config = Config(config_text) 
        items = ["statement", "checker", "description", "validator", "main_solution"]        
        for item in items:
            self.print_to_console(self.__get_item_status(item), item)
        tests_description_path = "tests.please"
        self.print_to_console(self.__get_item_status(path=tests_description_path), "tests desription")
        
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
            item_modification_time_sec = os.stat(item_path).st_mtime
            if (item_modification_time_sec > self.__folder_generation_time_sec+1 or
                item_modification_time_sec < self.__folder_generation_time_sec - 60*2): # please create problem can't
                                                                                        # work slower, than 2 minutes
                return("ok")
            else:
                return("warning")
        else:
            return("error")