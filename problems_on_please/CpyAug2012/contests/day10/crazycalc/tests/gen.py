#!/usr/bin/python3
from sys import argv
from random import randint
a, b = map(int, argv[1:3])
print(randint(a, b), randint(a, b))
