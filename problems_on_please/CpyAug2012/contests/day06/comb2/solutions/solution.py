#!/usr/bin/python3
from sys import *
setrecursionlimit(1000000)

fin = open('comb2.in', 'r')
fout = open('comb2.out', 'w')

def printArr(A):
    for elem in A:
        print(elem, end = ' ', file=fout)
    print(file=fout)


def gen(v, prefix):
    if v == len(prefix):
        printArr(prefix)
    else:
        if v == 0:
            i = 1
        else:
            i = prefix[v - 1] + 1
        while i <= k and k - i + 1 >= len(prefix) - v:
            prefix[v] = i
            gen(v + 1, prefix)
            i += 1

n, k = map(int, fin.read().strip().split())
prefix = [0] * n
gen(0, prefix)
