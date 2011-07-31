#!/usr/bin/python

class Base:
    ALL = -1
    def __init__(self, extensions_dict):
        self.__extensions = extensions_dict

    def extensions(self, type):
        if type == Base.ALL:
            all_extensions = []
            for _, extensions in self.__extensions.items():
                all_extensions += extensions
            return all_extensions
        else:
            return self.__extensions[type]
