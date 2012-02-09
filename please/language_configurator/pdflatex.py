import os
import os.path

from please.globalconfig import temp_statements_dir
from please.template.template_utils import get_template_full_path


def is_compilation_garbage(source):
    extensions = [".aux"]
    if os.path.splitext(source)[1] == '':
        return False
    extension = os.path.splitext(source)[1]
    return extension.lower() in extensions

class PDFLatexConfigurator:
    def get_run_command(self, source):
        bat_name = os.path.join("..", temp_statements_dir, 'maketex.bat')
        if not os.path.isfile(bat_name):
            batfile = open(bat_name, "w")
            batfile.write("REM ===USING png/jpg/jpeg/pdf PICTURES IN TEX===\n\n")
            for _ in range(2): #always run latex two times to get page numbers etc
                batfile.write("pdflatex -include-directory=" + get_template_full_path('') + " -output-format=pdf -interaction=nonstopmode -halt-on-error " + source + "\n")
            batfile.write("\n\nREM ===USING eps PICTURES OR NO PICTURES IN TEX===\n\n")
            for _ in range(2): #always run latex two times to get page numbers etc
                batfile.write("REM latex -include-directory=" + get_template_full_path('') + " " + source + "\n")
            batfile.write("REM dvips " + os.path.splitext(source)[0] + ".dvi" + "\n")
            batfile.write("REM ps2pdf " + os.path.splitext(source)[0] + ".ps" + "\n")
            batfile.close()
        return ["maketex.bat", ]        

    def is_compile_garbage (self, source):
        #return is_compilation_garbage(source)
        return False
    def get_binary_name(self, source):
        return [os.path.splitext(source)[0] + ".pdf"]

def get_pdflatex_configurator():
    return PDFLatexConfigurator()
