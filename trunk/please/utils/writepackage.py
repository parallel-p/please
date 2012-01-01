from .. import globalconfig
from ..svn import ProblemInSvn

def writepackage(text):
    with open("default.package", "w", encoding = "utf-8") as output_stream:
        output_stream.write(text)
    ProblemInSvn().update(globalconfig.default_package)
