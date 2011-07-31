#!/usr/bin/python

from . import base

class Programs(base.Base):
    CPP, PASCAL, PYTHON = range(3)
    def __init__(self):
        super(Programs, self).__init__({
            Programs.CPP : ["cpp", "c++"],
            Programs.PASCAL : ["pas", "dpr"],
            Programs.PYTHON : ["py"]
        })

if __name__ == "__main__":
    p = Programs()
    print(p.extensions(Programs.ALL))
    print(p.extensions(Programs.CPP))
    print(p.extensions(Programs.PASCAL))
    print(p.extensions(Programs.PYTHON))
