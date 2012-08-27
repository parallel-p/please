import os.path
from .. import globalconfig
from ..utils.exceptions import PleaseException

def getter(func):
    def get_wrapped(self, key, default = None):
        if key in self:
            return func(self[key])
        return default
    return get_wrapped

def setter(func):
    def set_wrapped(self, key, value):
        self.key = func(value)
    return set_wrapped

class Config:
    """
    Multilevel config parser with possibility of set, delete, formatting data,
    and saving comments of source
    """
    def __init__(self, text, counter=0, depth=0, file = None):
        """
            conf = Config(text_of_config_file)
        """

        def strict_divide(string, number_of_parts, delim):
            parts = string.split(delim, number_of_parts - 1)
            n = string.count(delim)
            for i in range(n + 1, number_of_parts):
                parts.append(None)
            return parts
 
        def parse_iterator(line):
            (key_value_part, comment) = strict_divide(line, 2, '#')
            key, value = strict_divide(key_value_part, 2, '=')
            key = key.strip()
            if (value != None):
                value = value.strip()
            return (key, value, comment)
        
        file = file or os.path.join(os.getcwd(), globalconfig.default_package)
        self.__changed = False
        self.__counter = counter
        self.__settings = {}
        self.__source = []
        self.__file = file
        self.repeating_keywords = ["solution", "problem"]
        self.list_keywords = ["expected", "possible", "well_done_test", \
                              "well_done_answer"]
        for key in self.repeating_keywords:
            if key in self.list_keywords:
                raise PleaseException("Key '" + key + "' is in repeating_keywords and list_keywords at the same time")     
        if(type(text) == str):
            text = text.splitlines()
        while self.__counter < len(text):
            key, value, comment = parse_iterator(text[self.__counter])
            new_value = None
            if (key != ''):
                if (key in self.__settings and key not in self.repeating_keywords):
                    raise PleaseException("Key '" + key + "' already in dictionary")
                if (key == "}"):
                    if(depth == 0):
                        raise PleaseException("Incorrect brackets sequence: depth = 0, but met '}'\nLine: " + str(self.__counter))
                    if(value != None):
                        raise PleaseException("Assigning to '}'\nLine: " + str(self.__counter))
                    if comment is not None: self.__source.append(["", comment, True])
                    break
                if (value == "{"):
                    new_value = Config(text, self.__counter + 1, depth + 1, file)
                    self.__counter = new_value.get_finally_counter()
                else:
                    new_value = value
                if (key in self.list_keywords):
                    if(type(new_value) == str):
                        new_value = list(map(str.strip, new_value.split(",")))
                        self.__settings.setdefault(key, []).extend(new_value)
                    else:
                        raise PleaseException("'list_keyword''s elements values must be strings")
                elif (key in self.repeating_keywords):
                    self.__settings.setdefault(key, []).append(new_value)
                else:
                    self.__settings[key] = new_value
            self.__source.append([key, comment, True])
            self.__counter += 1      
        if(depth != 0 and self.__counter >= len(text)):
            raise PleaseException("Incorrect brackets sequence: depth = " + str(depth) +
                                  ", but not met '}'\nLine: " + str(self.__counter))

    def __get_config_string(self, key, value, comment, depth, indent, paste_fin_bracket):
        line = ""
        line += key + " = {"
        if comment is not None: line += " #" + comment
        line += "\n" + value.get_text(False, depth, indent, paste_fin_bracket)
        return line
        
    def get_text(self, eofline=True, depth=0, indent=" "*4, paste_fin_bracket=False):
        """
        Returns string, which contains good level-formatted config file.
        Parameters:
            1) eofline - paste empty string to the end (True by default)
            2) depth - base depth level (0 by default <=> no indent for base level)
            3) indent ("    " by default)
        """
        dict_used = dict(zip(self.repeating_keywords, [-1] * len(self.repeating_keywords)))
        lines = []
        for key, comment, ifcount in self.__source:
            line = indent * depth
            key = str(key)
            if comment is not None: comment = str(comment)
            if ifcount == True:
                if key in self.__settings:
                    value = self.__settings[key]
                    if isinstance(value, Config):
                        line += self.__get_config_string(key, value, comment, depth+1, indent, True)
                        lines.append(line)
                        continue
                    elif type(value) is list:
                        if key in dict_used:
                            dict_used[key] += 1
                            if type(value[dict_used[key]]) == Config:
                                line += self.__get_config_string(key, value[dict_used[key]], comment, depth+1, indent, True)
                                lines.append(line)
                                continue
                            else: line += key + " = " + ", ".join(list(map(str, value[dict_used[key]])))
                        else: line += key + " = " + ", ".join(list(map(str, value)))
                    elif value is None:
                        line += key
                    else:
                        line += key + " = " + str(value)
                    if comment is not None: line += " #" + comment
                    lines.append(line)
                else:
                    assert(key == "")
                    if comment is not None:
                        line += "#" + comment
                    lines.append(line)
            else:
                if comment is not None:
                    line += "#" + comment
                    lines.append(line)
        if(paste_fin_bracket==True):
            lines.append(indent * (depth - 1) + "}")
        if(eofline == True): lines.append("") # to make a "\n" in the end of file
        return "\n".join(lines)

    def __contains__(self, item):
        return item in self.__settings
    
    def keys(self):
        return self.__settings.keys()

    def values(self):
        return self.__settings.values()

    def items(self):
        return self.__settings.items()

    def __delitem__(self, item):
        self.delete(item)
        
    def delete(self, item, iterator=None):
        """ 
        Deletes item by keyword. If iterator given, deletes i-th element of list
        Example:
            conf.delete("item", 2)
        """
        self.__changed = True
        if type(self.__settings[item]) == list:
            if iterator is None:
                for i in range(len(self.__settings[item]), 0, -1):
                    self.delete(item, i - 1)
            else:
                numerator = -1
                killed = False
                for i in range(len(self.__source)):
                    if self.__source[i][0] == item and self.__source[i][2] == True:
                        numerator += 1
                        if numerator == iterator:
                            deltype = type(self.__settings[item][iterator])
                            del self.__settings[item][iterator]
                            if self.__source[i][1] is None or deltype == Config:
                                del self.__source[i]
                            else:
                                self.__source[i][2] = False
                            killed = True
                            break
                if not killed:
                    raise PleaseException("Can't find by iterator = " + str(iterator))
        else:
            deltype = type(self.__settings[item])
            del self.__settings[item]
            for i in range(len(self.__source)):
                if self.__source[i][0] == item:
                    if deltype == Config:
                        del self.__source[i]
                    else:
                        self.__source[i][2] = False
                    break

    def __convert_separators(self, path):
        splitted = sum([x.split('\\') for x in path.split('/')], [])
        return os.path.join(*splitted)

    def __getitem__(self, item):
        #if you don't need to check correctness of values, rewrite function get
        if item == "checker":
            # if local checker doesnt exists, return path to global checkers dir
            checker = self.__settings.get(item)
            checker_local_path = self.__convert_separators(checker)
            checker_full_path = os.path.join(os.path.split(self.__file)[0], checker_local_path)
            if not os.path.exists(checker_full_path):
                checkers_dir = os.path.join(globalconfig.root, globalconfig.checkers_dir)
                root_checker_path = os.path.join(checkers_dir, checker_local_path)
                #if not os.path.exists(root_checker_path) or not os.path.isfile(root_checker_path):
                #    raise PleaseException("There is no file '{0}' in current directory and in intpleaernal Please checkers directory (config {1})".format(checker, self.__file))
                #else:
                return root_checker_path
            return checker_full_path
        elif item in ["source", "validator", "statement", "description", "main_solution", "solution"]:
            if item == "validator":
                return self.__settings.get(item)
#            if self.__settings.get(item) is None:
#                raise PleaseException("There is no item '{0}' in config {1}".format(item, self.__file))
            else:
                if not isinstance(self.__settings.get(item), str):
                    return self.__settings.get(item)
                path = self.__convert_separators(self.__settings.get(item))       
                full_path = os.path.join(os.path.split(self.__file)[0], path)
                #if not os.path.exists(full_path) or not os.path.isfile(full_path):
                #    raise PleaseException("There is no file '{1}' (item '{0}' in config {2})".format(item, full_path, self.__file))
                return path
        elif item in ["time_limit", "memory_limit"]:
            if self.__settings.get(item) is None:
                raise PleaseException("There is no item '{0}' in config {1}".format(item, self.__file))
            else:            
                limit = self.__settings.get(item)
                try:
                    value = float(limit)
                    if not (value > 0):
                        raise PleaseException("Limits in config {0} should be greater than 0".format(self.__file))
                except ValueError as ex:                
                    raise PleaseException("A problem occured while converting a value of item '{0}' in config {1} to float".format(item, self.__file))
                return limit
        elif item in ["input", "output", "shortname"]:
            if self.__settings.get(item) in [None, ""]:
                raise PleaseException("Items 'shortname', 'input' and 'output' in config {0} should be set".format(self.__file))
            return self.__settings.get(item)
        if item not in self.__settings and item in self.repeating_keywords + self.list_keywords:
            return []
        return self.__settings.get(item)

    def __setitem__(self, item, value):
        self.set(item, value)

    def set(self, item, value, comment=None, in_list=False):
        self.__changed = True
        if type(value) == str:
            value = value.strip()
        if item not in self.__settings:
            if in_list == True:
                self.__settings[item] = [value]
            else:
                self.__settings[item] = value
            self.__source.append([item, comment, True])
        else:
            if type(self.__settings[item]) == list and in_list == True:
                self.__source.append([item, comment, True])
                self.__settings[item].append(value)
            else:
                self.__settings[item] = value
            
    def get_finally_counter(self):
        return self.__counter
    
    def isChanged (self):
        return self.__changed

    def get(self, item, default = None):
        ret = self.__getitem__(item)
        if ret is not None:
            return ret
        else:
            return default
        #if item in self.__settings and self.__settings[item] is not None:
        #    return self.__settings[item]
        #else:
        #    return default

    get_path = getter(lambda path, _ossep = os.sep: path.replace('/', _ossep))
    set_path = setter(lambda path, _ossep = os.sep: path.replace(_ossep, '/'))

class ConfigFile(Config):
    def __init__(self, filename):
        self.filename = filename
        if os.path.isfile(filename):
            with open(filename, 'r', encoding = 'utf-8-sig') as f:
                text = f.read()
        else:
            text = ''
        super().__init__(text, file = filename)

    def write(self):
        with open(self.filename, 'w', encoding = 'utf-8') as f:
            f.write(self.get_text())

def create_simple_config(file_name, config):
    with open(file_name, 'w', encoding='utf-8') as file:
        write = lambda x: file.write(config[x] + '\n')
        write('shortname')
        write('name')
        write('input')
        write('output')
        write('time_limit')
        write('memory_limit')
        file.write(os.path.split(config['checker'])[-1] + '\n')
        if not 'id' in config:
            write('shortname')
        else:
            write('id')
