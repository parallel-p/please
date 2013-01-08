#!/bin/python3
import sys

inf = sys.stdin
ouf = sys.stdout


n, m = map(int, inf.readline().split())

a = [0] * n
dp = [[0 for j in range(m)] for i in range(n)]

for i in range(n):
        a[i] = list(map(int, inf.readline().split()))

ans = a[0][0]
dp[0][0] = a[0][0]
for i in range(1, n):
        dp[i][0] = a[i][0]
        ans = max(ans, dp[i][0])
for i in range(1, m):
        dp[0][i] = a[0][i]
        ans = max(ans, dp[0][i])
for i in range(n):
        for j in range(m):
                if a[i][j] == 1:
                        dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                        ans = max(ans, dp[i][j])
ouf.write("{0}\n".format(ans))
