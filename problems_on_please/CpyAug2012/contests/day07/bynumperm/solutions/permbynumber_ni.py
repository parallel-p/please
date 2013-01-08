#!/usr/bin/python3
import math

inf = open("bynumber.in", "r")
ouf = open("bynumber.out", "w")
n = int(inf.readline())
k = int(inf.readline())

a = set(i + 1 for i in range(n))

for i in range(n):
        cur = math.factorial(n - i - 1)
        for j in a:
                if k < cur:
                        ouf.write(str(j) + " ")
                        a.remove(j)
                        break
                else:
                        k -= cur
