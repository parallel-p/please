n = int(input())
D = [[0, 0, 0] for i in range(40)]
D[0] = [1, 1, 0]
for i in range(1, n):
    p = D[i - 1]
    D[i] = [p[0] + p[1] + p[2], p[0], p[1]]
print(sum(D[n - 1]))
