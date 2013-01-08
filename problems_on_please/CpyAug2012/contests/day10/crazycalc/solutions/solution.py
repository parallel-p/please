#!/usr/bin/python3
a, b = map(int, input().split())
nmx = 10000

def correct(x):
    return 0 < x and x < nmx

def edges(x):
    return filter(correct, [x - 2, 3 * x, x + sum(map(int, str(x)))])

from collections import deque
D = [-1] * nmx
def BFS(a, b):
    D[a] = 0
    Q = deque([a])
    while len(Q) > 0:
        v = Q.popleft()
        for u in edges(v):
            if D[u] == -1:
                D[u] = D[v] + 1
                Q.append(u)
BFS(a, b)
print(D[b])
