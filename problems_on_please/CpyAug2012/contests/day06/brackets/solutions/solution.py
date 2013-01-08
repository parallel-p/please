#!/usr/bin/python3
from sys import *
setrecursionlimit(100000)

fin = open('brackets.in', 'r')
fout = open('brackets.out', 'w')

def gen(prefix, n, cnt_open, cnt_close):
    if len(prefix) == 2 * n:
        print(prefix, file=fout)
    else:
        if n - cnt_open > 0:
            gen(prefix + '(', n, cnt_open + 1, cnt_close)
        if cnt_open - cnt_close > 0:
            gen(prefix + ')', n, cnt_open, cnt_close + 1)

n = int(fin.read().strip())
gen('', n, 0, 0)

fout.close()
