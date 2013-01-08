#!/usr/bin/python3
import sys
sys.setrecursionlimit(101000)

def DFS(start, G, Color, Path, Answer):
    Color[start] = 1
    for u in G[start]:
        if Color[u] is None:
            Path.append(u)
            DFS(u, G, Color, Path, Answer)
            Path.pop()
            if len(Answer) > 0:
                return
        elif Color[u] == 1:
            Answer.extend(Path[Path.index(u):])
            return
    Color[start] = 2

fin = open("cycle.in", "r")
fout = open("cycle.out", "w")

N, M = map(int, fin.readline().split())
G = [set() for i in range(N + 1)]
Color = [None] * (N + 1)
Answer = []


for i in range(M):
    a, b = map(int, fin.readline().split())
    G[a].add(b)
i = 1
for i in range(N, 0, -1):
    if Color[i] is None:
        DFS(i, G, Color, [i], Answer)
        if len(Answer) > 0:
            fout.write("YES\n")
            fout.write(str(len(Answer)) + "\n")
            fout.write(" ".join(map(str, Answer)))
            fout.write("\n")
            break
else:
    fout.write("NO\n")
fin.close()
fout.close()
