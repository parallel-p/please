#python3
import sys


inf = 10 ** 10

fin = open('gasstation.in')

x = list(map(int, fin.readline().rstrip().split()))
n = len(x)

a = [[inf] * (3 * n) for i in range(3 * n)]
for i in range(n):
    a[i][i + n] = x[i]
    a[i + n][i + 2 * n] = x[i]

for line in fin.readlines():
    first, second = map(lambda x: int(x) - 1, line.rstrip().split())
    a[first + n][second] = 0
    a[first + 2 * n][second + n] = 0
    a[second+n][first] = 0
    a[second + 2 * n][first + n] = 0

for k in range(3 * n):
    for i in range(3 * n):
        for j in range(3 * n):
            a[i][j] = min(a[i][j], a[i][k] + a[k][j])
print(a[0][n-1] if a[0][n - 1] < inf else -1, file = open('gasstation.out', 'w'))






