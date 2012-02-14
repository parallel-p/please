from .. import globalconfig

def writepackage(text):
    with open("default.package", "w", encoding = "utf-8") as output_stream:
        output_stream.write(text)