#!/dev/python3

fin = open('sequence.in', 'r')
fout = open('sequence.out', 'w')
a = list(map(int, fin.readline().split()))
n = len(a)
a = [1] + a
d = [0] * (n + 1)
for i in range(1, n + 1):
    d[i] = max([j[1] for j in enumerate(d[:i]) if a[i] % a[j[0]] == 0]) + 1
print(max(d), file=fout)
