import os
import os.path
def is_compilation_garbage(source):
    extensions = [".aux"]
    if os.path.splitext(source)[1] == '':
        return False
    extension = os.path.splitext(source)[1]
    return extension.lower() in extensions

class PDFLatexConfigurator:
    def get_run_command(self, source):
        return ["pdflatex", "-output-format=pdf", "-interaction=nonstopmode", source]
    def is_compile_garbage (self, source):
        #return is_compilation_garbage(source)
        return False
    def get_binary_name(self, source):
        return [os.path.splitext(source)[0] + ".pdf"]

def get_pdflatex_configurator():
    return PDFLatexConfigurator()