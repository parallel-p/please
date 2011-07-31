import unittest
from please.language_configurator.pdflatex import PDFLatexConfigurator
from please.language_configurator.pdflatex import get_pdflatex_configurator
from please.language_configurator.pdflatex import is_compilation_garbage

class PDFLatexConfiguratorTest(unittest.TestCase):
    def test_is_garbage(self):
        extensions_list =  extensions = [".log", ".aux"]
        
        pdflatex_configurator = PDFLatexConfigurator()
        
        #simple extension test
        for extension in extensions_list :
            self.assertFalse(pdflatex_configurator.is_compile_garbage("project" + extension))
        self.assertFalse(pdflatex_configurator.is_compile_garbage("\windows\documents\sample_file "))
        self.assertFalse(pdflatex_configurator.is_compile_garbage("\windows\documents\sample_file.tex"))
        #case tests
        self.assertFalse(pdflatex_configurator.is_compile_garbage("\windows\documents\sample_file.Tex"))
        self.assertFalse(pdflatex_configurator.is_compile_garbage("\windows\documents\sample_file.tEX"))
        self.assertFalse(pdflatex_configurator.is_compile_garbage("\windows\documents\sample_file.TEX"))
                         
                                     
    def test_get_run_command(self) :
        pdflatex_configurator = PDFLatexConfigurator()
        self.assertEqual(["pdflatex", "-output-format=pdf", "-interaction=nonstopmode", \
                          "project.tex"], pdflatex_configurator.get_run_command("project.tex"))
                
if __name__ == '__main__':
    unittest.main()
