import logging

mod_logger = logging.getLogger ("please_logger.matcher")

class Matcher:
    
    """
    Description:
    Stores all function-template relations

    m = Matcher()

    m.add_handler(Template(["add", "@types", "sol", "#file"]), add_solution)

    m.matches(["add", "wa", "tl", "sol", "sol.cpp"])
    output: add_solution #(function)
    """

    def __init__(self):
        self.__handlers = []

    def add_handler(self, template, function, has_access):
        """
            Assign specified function to a specified template.
            Template is any class with function corresponds
            with similar simantic as Template.
        """
        self.__handlers.append((template, function, has_access))

    def matches(self, args):
        """
            Calls the function that matches the query in "args"
            Throws exception if no or more then one
            templates correspons to args.
        """        
        
        _inst_logger = logging.getLogger("please_logger.matcher.Matcher.matches")
        
        function_args_found = None
        function_found = None
        function_found_in_not_acc = False
        _inst_logger.debug ("Matching...")
        for template, function, has_access in self.__handlers:
            function_args = template.corresponds(args)
            if function_args != None:
                # Make sure only one function corresponds to the arguments passed
                if has_access == True:
                    if function_found != None:
                        raise MatcherException("More than 1 functions match the template entered")
                    function_found, function_args_found = function, function_args
                else:
                    function_found_in_not_acc = True
                               

        if function_found == None:
            if function_found_in_not_acc == True:
                raise MatcherException("This command is not available. Probably, you try run command for problem modify out of its folder?")
            else:
                raise MatcherException("No functions match the template entered")
        
        _inst_logger.debug ("Run function: " + function_found.__name__ + ". Matching completed")
        
        return function_found(**function_args_found)

class MatcherException(Exception):
    pass

