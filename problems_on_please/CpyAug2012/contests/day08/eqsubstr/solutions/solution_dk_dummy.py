#!/usr/bin/python3

fin = open("eqsubstr.in", "r")
fout = open("eqsubstr.out", "w")

S = fin.readline().rstrip()
NQueries = int(fin.readline().rstrip())
result = []
for i in range(NQueries):
    l1, r1, l2, r2 = map(int, fin.readline().rstrip().split())
    if S[l1 - 1:r1] == S[l2 - 1:r2]:
        result.append("+")
    else:
        result.append("-")
fout.write("".join(result) + "\n")
fin.close()
fout.close()
