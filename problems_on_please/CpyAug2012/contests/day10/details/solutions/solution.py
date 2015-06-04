#!/usr/bin/python3
from sys import setrecursionlimit
setrecursionlimit(1000000)

C = list(map(int, input().split()))
n = len(C)
was = [False for i in range(n)]
E = []

gans = 0
def ans(x):
    global gans
    gans += C[x]
    was[x] = True
    for y in E[x]:
        if not was[y]:
            ans(y)

for i in range(n):
    E.append(set(map(lambda x : int(x) - 1, input().split())))
ans(0)
print(gans)
