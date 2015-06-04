#!/usr/bin/python3
from sys import argv
from random import randint 
n, mx = int(argv[1]), int(argv[2])
print(' '.join(map(str, [randint(1, mx) for i in range(n)])))
