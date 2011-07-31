import re
import os

def add_statement (default, lang, statement, path):
    """
       This function takes four arguments:
           default - dictionary containing default.package,
           lang - language. Created file will be named statements\statement."lang".tex .For example if lang = "ru"
       file name will be statements\statement.ru.tex
           statement - string, containing problem statement from polygon package (in .tex format)
           path - path to problem package
       Function doesn't return anything and creates file with problem statement in please format (semi-tex)
    """

    regexp = r"\\begin{problem}{(?P<name>.+?)}.+?$(?P<statement>.+?)\\Example(?P<examples>.+?)(^\\Note(?P<note>.+?))?^\\end{problem}"
    # fix for {XX megabytes} on second line
    lines = statement.splitlines()
    if re.match("^{[^{]*}$", lines[1]):
        lines.pop(1)
    fixed_statement = "\n".join(lines)

    matched = re.match(regexp, fixed_statement, re.MULTILINE | re.DOTALL)
    problem_statement = matched.group("statement")
    problem_note = matched.group("note")
    if problem_note is not None:
        problem_statement += "\n \\Note \n" + problem_note
    out_file  = open( os.path.join(path,"statements","statement."+lang+".tex"),"w", encoding = "UTF8")
    out_file.write(problem_statement)

    if not "statement" in default:
        default["statement"] = ""
    default["statement"] += "statements/statement." + lang + ".tex " + "# statements in other languages: " if default["statement"] == "" else "; "

    if not "name" in default:
        default["name"] = ""
    default["name"] += matched.group("name") + "# names in other languages: " if default["name"] == "" else "; "

#statement = open("problem.tex","r", encoding = "UTF-8").read()
#add_statement({},"ru",statement,"")
