import os
import os.path

from please.globalconfig import temp_statements_dir
from please.template.template_utils import get_template_full_path
from .language_configurator_utils import is_windows

def is_compilation_garbage(source):
    extensions = [".aux"]
    if os.path.splitext(source)[1] == '':
        return False
    extension = os.path.splitext(source)[1]
    return extension.lower() in extensions

class PSLatexConfigurator:
    def get_run_command(self, source):
        bat_name = os.path.join("..", temp_statements_dir, 'maketex')
        if is_windows():
            bat_name = bat_name + '.bat'
        remark = 'REM ' if is_windows() else '#'
        if not os.path.isfile(bat_name):
            batfile = open(bat_name, "w")
            if not is_windows():
                batfile.write('#!/bin/sh\nexport TEXINPUTS="' + get_template_full_path('') + ':.:"\n')
            batfile.write(remark + "===USING png/jpg/jpeg/pdf PICTURES IN TEX===\n\n")
            for _ in range(2): #always run latex two times to get page numbers etc
                batfile.write(remark + "pdflatex -include-directory=" + get_template_full_path('') + " -output-format=pdf -interaction=nonstopmode -halt-on-error " + source + "\n")
            batfile.write("\n\n" + remark + "===USING eps PICTURES OR NO PICTURES IN TEX===\n\n")
            for _ in range(2): #always run latex two times to get page numbers etc
                batfile.write("latex -include-directory=" + get_template_full_path('') + " " + source + "\n")
            batfile.write("dvips " + os.path.splitext(source)[0] + ".dvi" + "\n")
            batfile.write("ps2pdf " + os.path.splitext(source)[0] + ".ps" + "\n")
            batfile.close()
            os.chmod(bat_name, 755)
        if is_windows():
            return ["maketex.bat", ]
        else:
            return ["./maketex", ]


    def is_compile_garbage (self, source):
        #return is_compilation_garbage(source)
        return False

    def get_binary_name(self, source):
        return [os.path.splitext(source)[0] + ".pdf"]

def get_pslatex_configurator():
    return PSLatexConfigurator()
