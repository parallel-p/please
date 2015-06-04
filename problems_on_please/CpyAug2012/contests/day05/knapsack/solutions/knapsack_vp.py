#!/dev/python3

fin = open('knapsack.in', 'r')
fout = open('knapsack.out', 'w')

MAXS = 10001

s = int(fin.readline())
a = [False] * MAXS
a[0] = True
for i in map(int, fin.readline().split()):
    j = MAXS - i - 1
    while j >= 0:
        if a[j] == True:
            a[j + i] = True
        j -= 1
print(s - a[s::-1].index(True), file=fout)
