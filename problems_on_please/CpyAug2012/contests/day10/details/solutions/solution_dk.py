#!/usr/bin/python3
import sys

sys.setrecursionlimit(100000)

Edges = []
Times = []
IsVisited = []

def DFS(vertex):
    IsVisited[vertex] = True
    Ans = Times[vertex]
    for another in Edges[vertex]:
        if not IsVisited[another]:
            Ans += DFS(another)
    return Ans

Times = [0] + list(map(int, input().split()))
IsVisited = [False] * len(Times)
Edges = [0] * len(Times)
for i in range(1, len(Edges)):
    Edges[i] = set(map(int, input().split()))
print(DFS(1))


