#!/usr/bin/python3
n, m = map(int, input().split())
D = [-1] * n
E = [set() for i in range(n)]
par = [-1] * n
from collections import deque

def BFS(a, b):
    Q = deque([a])
    D[a] = 0
    while len(Q) != 0:
        v = Q.popleft()
        for u in E[v]:
            if (D[u] == -1):
                D[u] = D[v] + 1
                Q.append(u)
                par[u] = v

a, b = map(lambda x : int(x) - 1, input().split())
for i in range(m):
    p, q = map(int, input().split())
    E[p - 1].add(q - 1)
    E[q - 1].add(p - 1)
BFS(a, b)
print(D[b])
if (D[b] != -1):
    L = [b]
    q = D[b]
    for i in range(q):
       b = par[b]
       L.append(b)
    assert b == a
    print(' '.join(map(lambda x : str(x + 1), reversed(L))))


