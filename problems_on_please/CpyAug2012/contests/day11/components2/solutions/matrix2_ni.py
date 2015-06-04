#python3
import sys

sys.setrecursionlimit(640000000)
inf = open("components2.in", "r")


n, m = [int(x) for x in inf.readline().split()]
edg = [0] * n
comp = [0] * n
was = [0] * n
for i in range(n):
        edg[i] = []
        comp[i] = []

for i in range(m):
        u, v = [int(x) - 1 for x in inf.readline().split()]
        edg[u].append(v)
        edg[v].append(u)

res = 0

def dfs(v):
        was[v] = 1
        comp[res - 1].append(str(v + 1))
        for i in edg[v]:
                if was[i] == 0:
                        dfs(i)

for i in range(n):
        if was[i] == 0:
                res += 1
                dfs(i)

ouf = open("components2.out", "w")
ouf.write(str(res) + "\n")
for i in range(res):
        ouf.write(str(len(comp[i])) + "\n")
        ouf.write(" ".join(comp[i]) + "\n")
