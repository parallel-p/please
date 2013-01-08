#python3
from sys import stdin, stdout

inf = stdin
ouf = stdout

m, n = map(int, inf.readline().split())

a = list([0] * (n + 2) for x in range(m + 2))

a[0][0] = 1

for i in range(0, m):
        for j in range(0, n):
                a[i + 1][j + 2] += a[i][j]
                a[i + 2][j + 1] += a[i][j]

ouf.write(str(a[m - 1][n - 1]))

inf.close()
ouf.close()
