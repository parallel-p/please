class WordMistake:
    @staticmethod
    def differents(a, b):
        """Returns number of different
           letters in two words of the same length"""
        return [x == y for x, y in zip(a, b)].count(False)

    @staticmethod
    def one_change_letter(a, b):
        """Returns True if words has exactly one changed letter"""
        return len(a) == len(b) and WordMistake.differents(a, b) <= 1

    @staticmethod
    def one_add_letter(a, b):
        """Returns True if it is possible to add one letter to a to get b"""
        if len(a) != len(b) - 1:
            return False
        for i in range(len(a) + 1):
            if WordMistake.differents(a[:i] + '?' + a[i:], b) <= 1:
                return True

    @staticmethod
    def one_del_letter(a, b):
        """Returns True if it is possible to del one letter to a to get b"""
        return WordMistake.one_add_letter(b, a)

    @staticmethod
    def one_swap_letter(a, b):
        """Returns True if it is possible to swap two sequent
           letters in a to get b"""
        if len(a) != len(b):
            return False
        for i in range(len(a) - 1):
            swap_a = a[:i] + a[i + 1] + a[i] + a[i+2:]
            if swap_a == b:
                return True
        return False

class WordTemplate :
    """
    Description :
    There are 2 methods :
       corresponds  - it checks if our word is in the command template
          Example: word_template = WordTemplate("solution|sol")
                   word_template.corresponds(solution)
                   >>> TRUE
       mistake_corresponds - it checks if our word
            is in the command template if it has 1 mistake

       Author : Alexander Podolskiy
    """
    def __init__(self, template) :
        self.command_list = template.split("|")

    def corresponds (self, word) :
        return word in self.command_list

    def mistake_corresponds (self, word) :
        """
        If word has 1 mistake this method will replace it.
        This types of mistakes are supported :
        1 - one symbol is different
        2 - two next symboles are swapped
        3 - one symbol is missed
        4 - one symbol is added
        """
        if self.corresponds(word) :
            return True
        else :
            for command in self.command_list :
                if WordMistake.one_change_letter(word, command):
                    return True
                if WordMistake.one_add_letter(word, command):
                    return True
                if WordMistake.one_del_letter(word, command):
                    return True
                if WordMistake.one_swap_letter(word, command):
                    return True
            return False

