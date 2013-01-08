#!/usr/bin/python3
inf = open("baobab.in", "r")

n = int(inf.readline())
a = [0] * n
was = [0] * n
for i in range(n):
        a[i] = [int(x) for x in inf.readline().split()]


def dfs(v):
        was[v] = 1;
        for i in range(n):
                if a[v][i] == 1 and was[i] == 0:
                        dfs(i)
cnt = 0
for i in range(n):
        for j in range(i):
                cnt += a[i][j]
good = (cnt == n - 1)
dfs(0)
for i in range(n):
        good = good and (was[i] == True)
ouf = open("baobab.out", "w")
if good: ouf.write("YES")
else: ouf.write("NO")
