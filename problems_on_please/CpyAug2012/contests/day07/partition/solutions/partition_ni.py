#!/usr/bin/env python3


inp = open('partition.in', 'r')
out = open('partition.out', 'w')
n = int(inp.readline().split()[0])

a = [0] * (n + 1)
def rec(n, lst, pos):
        #print("n = ", n, "lst = ", lst, "pos = ", pos)
        if (n == 0):
                s = ""
                for i in range(0, pos):
                        s += str(a[i]) + " "
                out.write(s + "\n")
                return
        j = min(n, lst)
        for i in range(1, j + 1):
                a[pos] = i
                rec(n - i, min(lst, i), pos + 1)
rec(n, n, 0)
inp.close()
out.close()

