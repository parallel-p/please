#!/usr/bin/python3
import random
def qsorted(A):
    if len(A) <= 1:
        return A
    q = random.choice(A)
    L = []
    M = []
    R = []
    for elem in A:
        if elem < q:
            L.append(elem)
        elif elem > q:
            R.append(elem)
        else:
            M.append(elem)
    return qsorted(L) + M + qsorted(R)

A = list(map(int, open('qsort.in', 'r').read().strip().split()))
print(' '.join(map(str, qsorted(A))), file=open('qsort.out', 'w'))
