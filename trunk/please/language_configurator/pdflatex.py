import os
import os.path

from ..globalconfig import temp_statements_dir
from ..template.template_utils import get_template_full_path
from .language_configurator_utils import is_windows

def is_compilation_garbage(source):
    if os.path.splitext(source)[1] == '':
        return False
    extension = os.path.splitext(source)[1]
    return extension.lower() in {'aux'}

class PDFLatexConfigurator:
    def get_compile_command(self, source):
        return (['pdflatex', '-output-format=pdf', '-interaction=nonstopmode', '-draftmode', source],
                ['pdflatex', '-output-format=pdf', '-interaction=nonstopmode', source])

    def is_compile_garbage (self, source):
        #return is_compilation_garbage(source)
        return False

    def get_binary_name(self, source):
        return [os.path.splitext(source)[0] + ".pdf"]

def get_pdflatex_configurator():
    return PDFLatexConfigurator()
