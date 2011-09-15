import os.path
from .. import globalconfig

class ConfigException(Exception):
    pass

class Config:
    """
    Very cool multilevel config parser with possibility of set, delete, formatting data,
    and saving comments of source
    """
    def __init__(self, text, counter=0, depth=0):
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

        self.__changed = False
        self.__counter = counter
        self.__settings = {}
        self.__source = []
        self.repeating_keywords = ["solution"]
        self.list_keywords = ["expected_verdicts", "possible_verdicts"]
        for key in self.repeating_keywords:
            if key in self.list_keywords:
                raise ConfigException("Key '" + key + "' is in repeating_keywords and list_keywords at the same time")     
        if(type(text) == str):
            text = text.splitlines()
        while self.__counter < len(text):
            key, value, comment = parse_iterator(text[self.__counter])
            new_value = None
            if (key != ''):
                if (key in self.__settings and key not in self.repeating_keywords):
                    raise ConfigException("Key '" + key + "' already in dictionary")
                if (key == "}"):
                    if(depth == 0):
                        raise ConfigException("Incorrect brackets sequence: depth = 0, but met '}'\nLine: " + str(self.__counter))
                    if(value != None):
                        raise ConfigException("Assigning to '}'\nLine: " + str(self.__counter))
                    if comment is not None: self.__source.append(["", comment, True])
                    break
                if (value == "{"):
                    new_value = Config(text, self.__counter + 1, depth + 1)
                    self.__counter = new_value.get_finally_counter()
                else:
                    new_value = value
                if (key in self.list_keywords):
                    if(type(new_value) == str):
                        new_value = list(map(str.strip, new_value.split(",")))
                        self.__settings.setdefault(key, []).extend(new_value)
                    else:
                        raise ConfigException("'list_keyword''s elements values must be strings")
                elif (key in self.repeating_keywords):
                    self.__settings.setdefault(key, []).append(new_value)
                else:
                    self.__settings[key] = new_value
            self.__source.append([key, comment, True])
            self.__counter += 1      
        if(depth != 0 and self.__counter >= len(text)):
            raise ConfigException("Incorrect brackets sequence: depth = " + str(depth) + 
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
                    if type(value) == Config:
                        line += self.__get_config_string(key, value, comment, depth+1, indent, True)
                        lines.append(line)
                        continue
                    elif type(value) == list:
                        if key in dict_used:
                            dict_used[key] += 1
                            if type(value[dict_used[key]]) == Config:
                                line += self.__get_config_string(key, value[dict_used[key]], comment, depth+1, indent, True)
                                lines.append(line)
                                continue
                            else: line += key + " = " + ", ".join(list(map(str, value[dict_used[key]])))
                        else: line += key + " = " + ", ".join(list(map(str, value)))
                    elif value is None: line += key
                    else: line += key + " = " + str(value)
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
                    raise ConfigException("Can't find by iterator = " + str(iterator))
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
        splitted = path.split('/')
        return os.path.join(*splitted)

    def __getitem__(self, item):
        if item == "checker":
            # if local checker doesnt exists, return path to global checkers dir
            checker = self.__settings.get(item)
            checker_local_path = self.__convert_separators(checker)
            if not os.path.exists(checker_local_path):
                return os.path.join(globalconfig.root, globalconfig.checkers_dir, checker_local_path)
            return checker_local_path
        elif item in ["source", "validator", "statement", "description", "main_solution"] and self.__settings.get(item) is not None:
            return self.__convert_separators(self.__settings.get(item))
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
