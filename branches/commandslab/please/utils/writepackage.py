from .. import globalconfig
import os

def writepackage(text):
    with open(globalconfig.default_package,
              "w", encoding = "utf-8") as output_stream:
        output_stream.write(text)
