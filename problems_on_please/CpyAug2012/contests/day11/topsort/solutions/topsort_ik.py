#!/usr/bin/python3
from sys import exit
file_in = open("topsort.in", "r");
file_out = open("topsort.out", "w");


def visit(u):
    visited[u] = 1
    for v in graph[u]:
        if visited[v] == 0:
            visit(v)
        elif visited[v] == 1:
            print(-1, file=file_out)
            file_out.close()
            exit(0)
    visited[u] = 2
    answer.append(u + 1)


n, m = [int(x) for x in file_in.readline().strip().split()]
graph = []
for i in range(n):
    graph.append([])
visited = [0] * n
answer = []

for i in range(m):
    u, v = [int(x) for x in file_in.readline().strip().split()]
    graph[u - 1].append(v - 1)

for i in range(n):
    if visited[i] == 0:
        visit(i)

for i in reversed(answer):
    print(i, end=" ", file=file_out)
