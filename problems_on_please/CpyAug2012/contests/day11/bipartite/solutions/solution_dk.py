#!/usr/bin/python3
import sys

def DFS(start, G, Color):
    if Color[start] is None:
        Color[start] = 1
    for u in G[start]:
        if Color[u] is None:
            Color[u] = 3 - Color[start]
            if not DFS(u, G, Color):
                return False
        elif Color[u] == Color[start]:
            return False
    return True

fin = open('bipartite.in', 'r')

N, M = map(int, fin.readline().split())
G = [set() for i in range(N + 1)]
Color = [None] * (N + 1)
for i in range(M):
    a, b = map(int, fin.readline().split())
    G[a].add(b)
    G[b].add(a)

i = 1
while i <= N and (Color[i] is not None or DFS(i, G, Color)):
    i += 1
if i <= N:
    open('bipartite.out', 'w').write("NO\n")
else:
    open('bipartite.out', 'w').write("YES\n")

