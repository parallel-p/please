#!/usr/bin/python3
import io
inf = open("nextcomb.in", "r")
ouf = open("nextcomb.out", "w")
n, k = [int(x) for x in inf.readline().split()]
a = [int(x) for x in inf.readline().split()]

pos = k - 1
while pos >= 0 and a[pos] == n + pos - k + 1:
        pos -= 1

if pos == -1:
        ouf.write("0")
else:
        a[pos] += 1
        for i in range(pos + 1, k):
                a[i] = a[i - 1] + 1
        for i in range(k):
                a[i] = str(a[i])
        ouf.write(" ".join(a))
