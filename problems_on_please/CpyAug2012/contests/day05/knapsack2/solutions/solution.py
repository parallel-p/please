#python3
fin = open('knapsack2.in', 'r')
fout = open('knapsack2.out', 'w')

m = int(fin.readline().strip())
dp = []
inf = 0

w = fin.readline().split()
c = fin.readline().split()
n = len(w)

for i in range(n):
    w[i] = int(w[i])
    c[i] = int(c[i])

for i in range(n):
    dp.append([])
    for j in range(m + 1):
        dp[i].append(0)

for i in range(m):
    if w[0] <= i + 1:
        dp[0][i + 1] = c[0]

   
for i in range(1, n):
    for j in range(1, m + 1):
        if (j - w[i] >= 0) and (dp[i - 1][j - w[i]] + c[i] > dp[i - 1][j]):
            dp[i][j] = dp[i - 1][j - w[i]] + c[i]
        else:
            dp[i][j] = dp[i - 1][j]
            
i = n - 1
j = dp[n - 1][m]
k = m

while i >= 0 and (j != 0):
    #fout.write(str(j))
    while (i >= 0) and (dp[i][k] == j):
        i -= 1
    fout.write(str(i + 2) + ' ')
    j -= c[i + 1]
    k -= w[i + 1]
    while (i >= 0) and (dp[i][k] != j):
        i -= 1
    #fout.write(str(i))

#fout.write(str(dp))


fin.close()
fout.close()
