#!/usr/bin/python3

fin = open('tickets.in', 'r')
fout = open('tickets.out', 'w')

A = [list(map(int, i.split())) for i in fin.read().strip().split("\n")]

n = len(A)

D = [10**10] * (n + 1)
D[0] = 0
for i in range(n):
    for j in range(1, 4):
        if i + j > n:
            continue
        D[i + j] = min(D[i + j], D[i] + A[i][j - 1])

print(D[n], file=fout)
