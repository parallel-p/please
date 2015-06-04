#!/usr/bin/python3

fin = open('numbers.in', 'r')
fout = open('numbers.out', 'w')

def gen(n, k, prefix):
    if n == 0:
        print(" ".join(map(str, prefix)), file=fout)
        return
    for i in range(k):
        gen(n - 1, k, prefix + [i])

n, k = map(int, fin.read().strip().split())
gen(n, k, [])

