#!/usr/bin/python3

fin = open("maxcommonsubstr.in", "r")
fout = open("maxcommonsubstr.out", "w")

A = fin.readline().rstrip()
B = fin.readline().rstrip()

def Solve(L, A, B):
    for i in range(L, len(A) + 1):
        for j in range(L, len(B) + 1):
            if A[i - L:i] == B[j - L:j]:
                return True
    return False

left = 0
right = min(len(A), len(B)) + 1
while right - left > 1:
    middle = (left + right) // 2
    if Solve(middle, A, B):
        left = middle
    else:
        right = middle
fout.write(str(left) + "\n")
fin.close()
fout.close()
