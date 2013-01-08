#!/usr/bin/python3
from random import randint as rnd
from sys import argv
n, m = map(int, argv[1:3])
print(n, m)
print(rnd(1, n), rnd(1, n))
for i in range(m):
    a = rnd(1, n)
    b = a
    while (b == a):
        b = rnd(1, n)
    print(a, b)


