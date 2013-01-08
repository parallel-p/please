#!/usr/bin/python3

fin = open("commonsubstr.in", "r")
fout = open("commonsubstr.out", "w")

A = fin.readline().rstrip()
B = fin.readline().rstrip()

def Solve(L, A, B):
    Hashes = set()
    for i in range(L, len(A) + 1):
        Hashes.add(A[i - L:i])
    for i in range(L, len(B) + 1):
        if B[i - L:i] in Hashes:
            return True
    return False

L = int(fin.readline().rstrip())
if Solve(L, A, B):
    fout.write("YES\n")
else:
    fout.write("NO\n")
fin.close()
fout.close()
