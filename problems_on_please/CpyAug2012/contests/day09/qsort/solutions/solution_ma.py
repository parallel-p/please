#!/usr/bin/python3
from random import choice

def qsort(L):
    if len(L) <= 1:
        return L
    f = choice(L)
    less = []
    equal = []
    greater = []
    for x in L:
        if (x < f):
            less.append(x)
        elif (x == f):
            equal.append(x)
        else:
            greater.append(x)
    return qsort(less) + equal + qsort(greater)
    
A = list(map(int, open('qsort.in', 'r').read().strip().split()))
print(' '.join(map(str, qsort(A))), file=open('qsort.out', 'w'))
        
