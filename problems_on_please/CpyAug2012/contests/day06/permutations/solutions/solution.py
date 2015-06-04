#!/usr/bin/python3
from sys import *
setrecursionlimit(1000000)

fin = open('permutations.in', 'r')
fout = open('permutations.out', 'w')

def printArr(A):
    print(" ".join(list(map(str, A))), file=fout)


def gen(n, prefix, Was):
    if len(prefix) == n:
        printArr(prefix)
    else:
        for i in range(n):
            if not Was[i]:
                Was[i] = True
                gen(n, prefix + [i + 1], Was)
                Was[i] = False

n = int(fin.read().strip())
Was = [False] * n
gen(n, [], Was)
