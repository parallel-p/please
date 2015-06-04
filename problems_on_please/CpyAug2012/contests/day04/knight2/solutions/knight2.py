#python3
from sys import stdin, stdout
inf = stdin
ouf = stdout


m, n = map(int, inf.readline().split())

a = list(map(lambda x : list(map(lambda y : 0, range(0, n + 2))), range(0, m + 2)))

a[0][0] = 1

for i in range(0, m + n):
    for j in range(0, i + 1):
        x = i - j
        y = j
        if (x < m) and (y < n):
            a[x + 1][y + 2] += a[x][y]
            a[x + 2][y + 1] += a[x][y]
            if y > 0:
                a[x + 2][y - 1] += a[x][y]
            if x > 0:
                a[x - 1][y + 2] += a[x][y]

ouf.write(str(a[m - 1][n - 1]))

inf.close()
ouf.close()
