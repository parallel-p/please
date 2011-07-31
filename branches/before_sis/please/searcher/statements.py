import os.path

class Statements:
    def __init__(self, file_system):
        self.__file_system = file_system

    def file(self):
        """Returns path to statements or None"""
        tex_files = list(
            self.__file_system.find("statements", ".*\.tex", depth = 2))
        if len(tex_files) == 0:
            return None
        if len(tex_files) == 1:
            return tex_files[0]
        
        defaults = [tex for tex in tex_files
                    if os.path.basename(tex).startswith("default")]
        if len(defaults) == 0:
            return None
        if len(defaults) == 1:
            return defaults[0]
        for lang in ["", ".ru", ".en"]:
            defaults_lang = [tex for tex in defaults
                if os.path.basename(tex) == "default" + lang + ".tex"]
            if len(defaults_lang) == 1:
                return defaults_lang[0]
            if len(defaults_lang) != 0:
                return None #several default statements with specified language

        for candidate in [os.path.join("statements", "statements.tex"),
                          os.path.join("statements", "statement.tex")]:
            if self.__file_system.exists(candidate):
                return candidate

        return None#Sorry, I make all, what I can :(
