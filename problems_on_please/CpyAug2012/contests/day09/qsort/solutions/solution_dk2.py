#!/usr/bin/python3
import random
def qsorted(A):
    if len(A) <= 1:
        return A
    q = random.choice(A)
    L = [elem for elem in A if elem < q]
    M = [q] * A.count(q)
    R = [elem for elem in A if elem > q]
    return qsorted(L) + M + qsorted(R)

A = list(map(int, open('qsort.in', 'r').read().strip().split()))
print(' '.join(map(str, qsorted(A))), file=open('qsort.out', 'w'))


