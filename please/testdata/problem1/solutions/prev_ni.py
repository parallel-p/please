#!/usr/bin/python3
import io
inf = open("prev.in", "r")
n = int(inf.readline())
a = [int(x) for x in inf.readline().split()]

pos = n - 2
while (pos >= 0 and a[pos] < a[pos + 1]):
        pos -= 1

if pos == -1:
        for i in range(n):
                a[i] = str(n - i)
else:
        pos2 = pos + 1
        for i in range(pos + 1, n):
                if a[i] < a[pos] and a[pos2] < a[i]:
                        pos2 = i
        a[pos], a[pos2] = a[pos2], a[pos]
        a[(pos + 1):] = reversed(a[(pos + 1):])
        for i in range(n):
                a[i] = str(a[i])

ouf = open("prev.out", "w")
ouf.write(" ".join(a))
