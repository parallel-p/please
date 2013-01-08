#!/usr/bin/python3
from sys import argv
from random import randint as rnd
n = int(argv[1])
print(n, rnd(1, n))
for i in range(n):
    for j in range(n):
        print(0 if rnd(0, 10000) / 10000 > 3 / n else 1, end=' ' if j != n - 1 else '\n')
 
