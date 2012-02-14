import unittest
from please.lang_config.pdflatex import (get_config,
                                         is_compilation_garbage)

class PDFLatexConfiguratorTest(unittest.TestCase):
    def test_is_garbage(self):
        extensions_list =  extensions = [".log", ".aux"]
        
        config = get_config()('sample_file.tex')
        
        is_garbage = config.is_compile_garbage
        #simple extension test
        for extension in extensions_list :
            self.assertFalse(is_garbage("sample_file" + extension))
        self.assertFalse(is_garbage("\windows\documents\sample_file.pdf"))
        self.assertFalse(is_garbage("\windows\documents\sample_file.tex"))
        #case tests
        self.assertFalse(is_garbage("\windows\documents\sample_file.Tex"))
        self.assertFalse(is_garbage("\windows\documents\sample_file.tEX"))
        self.assertFalse(is_garbage("\windows\documents\sample_file.TEX"))
                         
                                     
    #def test_get_run_command(self) :
    #    pdflatex_configurator = PDFLatexConfigurator()
    #    self.assertEqual(["pdflatex", "-output-format=pdf", "-interaction=nonstopmode",
    #                      "-halt-on-error",
    #                      "project.tex"], pdflatex_configurator.get_run_command("project.tex"))
                
if __name__ == '__main__':
    unittest.main()
