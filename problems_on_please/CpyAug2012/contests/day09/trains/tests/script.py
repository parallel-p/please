from random import randint as rnd

n, k = map(int, input().split())
print(n)
L = []
for i in range(k):
    a, b = map(int, input().split())
    name = ''.join([chr(rnd(ord('a'), ord('z'))) for j in range(5)])
    L.append((a, -1, '+' + name))
    L.append((b, 1, '-' + name))
L = sorted(L)
for f in L:
    print(f[2])

