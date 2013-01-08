#!/usr/bin/python3

fin = open('fibseq.in', 'r')
fout = open('fibseq.out', 'w')

def printArr(A):
    for elem in A:
        print(elem, end = ' ', file=fout)
    print(file=fout)


def gen(v, prefix):
    if len(prefix) == v:
        printArr(prefix)
    else:
        prefix[v] = 0
        gen(v + 1, prefix)
        if v == 0 or prefix[v - 1] == 0:
            prefix[v] = 1
            gen(v + 1, prefix)

n = int(fin.read().strip())
prefix = [0] * n
gen(0, prefix)
