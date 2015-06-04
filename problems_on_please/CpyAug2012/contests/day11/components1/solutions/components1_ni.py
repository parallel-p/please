inf = open("components1.in", "r")

n = int(inf.readline())
a = []
was = [0] * n
for i in range(n):
        a.append([int(x) for x in inf.readline().split()])


def dfs(v):
        was[v] = 1
        for i in range(n):
                if a[v][i] == 1 and was[i] == 0:
                        dfs(i)
res = 0
for i in range(n):
        if was[i] == 0:
                res += 1
                dfs(i)
ouf = open("components1.out", "w")
ouf.write(str(res))
