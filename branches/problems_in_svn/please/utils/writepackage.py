from .. import globalconfig
from ..svn import ProblemInSvn

def writepackage(text):
    output_stream = open("default.package", "w", encoding = "utf-8")
    output_stream.write(text)
    output_stream.close()
    ProblemInSvn().update(globalconfig.default_package)
