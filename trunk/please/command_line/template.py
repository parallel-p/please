import logging
import os


from please.command_line.word_template import WordTemplate

mod_logger = logging.getLogger ("please_logger.template")

class Template:
    """
        Description....

        t = Template(["add", "@types", "sol", "#file"])
        dict = t.corresponds('.', ["add", "wa", "tl", "sol", "sol.cpp"])
        for k, v in dict.items():
            print(k, v)
        output:
            types ["wa", "tl"]
            file "sol.cpp"
    """

    def __is_args_list(self, word):
        return word.startswith("@")

    def __is_argument(self, word):
        return word.startswith("#")

    def __is_path(self, word):
        return word.startswith("$")

    def __is_regular(self, word):
        return not self.__is_args_list(word) and not self.__is_argument(word) and not self.__is_path(word)

    def __match(self, template, arg):
        return WordTemplate(template).mistake_corresponds(arg)

    def __check_correct(self, template):
        """Checks, that there are no two @ consequent or @#"""
        for i, cur_word in enumerate(template[:-1]):
            next_word = template[i + 1]
            if self.__is_args_list(cur_word) and not self.__is_regular(next_word):
                return True
        return False

    def __init__(self, template):
        if self.__check_correct(template):
            raise Exception ("The template contains @@ or @#")
        self.__template = template + ["^^^"]

    def corresponds (self, startdir, args):
        """
            Returns dictionary {argument : value} for each not regular element
            (starts with @ or #).
            value for @ is a list
            value for # is an element
        """
        
        _inst_logger = logging.getLogger ("please_logger.template.Template.corresponds")
        
        _inst_logger.debug("checking for a match. Template: "+" ".join(self.__template)+". String: "+" ".join(args))
        
        
        args_idx = 0
        res_dict = { }
        args = args + ["^^^"]
        for template_idx, template_entry in enumerate(self.__template):
            if args_idx == len(args):
                _inst_logger.debug("No coincidence")
                return None
            if self.__is_regular(template_entry):
                if (self.__match(template_entry, args[args_idx])):
                    args_idx += 1
                else:
                    _inst_logger.debug("No coincidence")
                    return None
            elif self.__is_argument(template_entry):
                res_dict[template_entry[1:]] = args[args_idx]
                args_idx += 1
            elif self.__is_path(template_entry):
                res_dict[template_entry[1:]] = os.path.abspath(os.path.join(startdir,args[args_idx]))
                args_idx += 1
            else:
                next_template = self.__template[template_idx + 1]
                next_args_idx = None
                for i in range(args_idx, len(args)):
                    if self.__match(next_template, args[i]):
                        next_args_idx = i
                        break
                if next_args_idx is None or next_args_idx == args_idx:
                    _inst_logger.debug("No coincidence")
                    return None
                res_dict[template_entry[1:]] = args[args_idx:next_args_idx]
                args_idx = next_args_idx
        _inst_logger.debug("Coincidence")
        return res_dict

