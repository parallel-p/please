from .. import globalconfig
from .. import svn

def writepackage(text, insvn = None):
    if insvn is None:
        insvn = svn.ProblemInSvn() 
    output_stream = open("default.package", "w", encoding = "utf-8")
    output_stream.write(text)
    output_stream.close()
    insvn.update(globalconfig.default_package)
