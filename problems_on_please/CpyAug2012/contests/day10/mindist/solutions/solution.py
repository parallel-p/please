#!/usr/bin/python3
inf = open("mindist.in", "r")

n, s = map(int, inf.readline().split())
s -= 1
a = []
for i in range(n):
    a.append([j for j, x in enumerate(inf.readline().split()) if x == "1"])

D = [-1] * n

from collections import deque

def bfs(s):
    Q = deque([s])
    D[s] = 0
    while len(Q) > 0:
        v = Q.popleft()
        for u in a[v]:
            if D[u] == -1:
                D[u] = D[v] + 1
                Q.append(u)


bfs(s)
print(' '.join(map(str, D)), file=open("mindist.out", 'w'))
