#!/usr/bin/python3

fin = open("commonsubstr.in", "r")
fout = open("commonsubstr.out", "w")

A = fin.readline().rstrip()
B = fin.readline().rstrip()

def Solve(L, A, B):
    for i in range(L, len(A) + 1):
        for j in range(L, len(B) + 1):
            if A[i - L:i] == B[j - L:j]:
                return True
    return False

L = int(fin.readline().rstrip())
if Solve(L, A, B):
    fout.write("YES\n")
else:
    fout.write("NO\n")
fin.close()
fout.close()


