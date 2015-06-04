#!/usr/bin/env python3

fin = open('lcs.in')
fout = open('lcs.out', 'w')

a = list(map(int, fin.readline().split()))
n = len(a)
b = list(map(int, fin.readline().split()))
m = len(b)

lcs = [[0] * (m + 1) for i in range(n + 1)]
answer = []

for i in range(n):
    for j in range(m):
        if a[i] == b[j]:
            lcs[i][j] = lcs[i - 1][j - 1] + 1
        else:
            lcs[i][j] = max(lcs[i - 1][j], lcs[i][j - 1])

i = n - 1
j = m - 1
while i != -1 and j != -1:
        if a[i] == b[j]:
                answer.append(a[i])
                i -= 1
                j -= 1
        else:
                if(lcs[i - 1][j] > lcs[i][j - 1]):
                        i -= 1
                else:
                        j -= 1

print(lcs[n - 1][m - 1], file=fout)
print(*answer[::-1], file=fout)

fin.close()
fout.close()
