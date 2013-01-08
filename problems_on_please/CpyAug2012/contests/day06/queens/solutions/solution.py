#!/usr/bin/python3
from sys import *
setrecursionlimit(100000)

fin = open('queens.in', 'r')
fout = open('queens.out', 'w')

def gen(Vertical, PlusDiagonal, MinusDiagonal, k, n):
    if k == n:
        global ans
        ans += 1
    else:
        for j in range(n):
            if not Vertical[j] and not PlusDiagonal[k + j] and not MinusDiagonal[k - j]:
                Vertical[j] = True
                PlusDiagonal[k + j] = True
                MinusDiagonal[k - j] = True
                gen(Vertical, PlusDiagonal, MinusDiagonal, k + 1, n)
                Vertical[j] = False
                PlusDiagonal[k + j] = False
                MinusDiagonal[k - j] = False

n = int(fin.read().strip())

ans = 0

Vertical = [False] * n
PlusDiagonal = [False] * (2 * n)
MinusDiagonal = [False] * (2 * n)

gen(Vertical, PlusDiagonal, MinusDiagonal, 0, n)

print(ans, file=fout)
