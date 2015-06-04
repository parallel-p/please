#!/usr/bin/python3                                       
from io import *

inf = open(file = 'dictionary.in', mode = 'r')
ouf = open(file = 'dictionary.out', mode = 'w')
Diction = dict()
for l in inf.readlines():
    line = l.split()
    for j in range(2, len(line) - 1):
        if line[j][:-1] not in Diction:
            Diction[line[j][:-1]] = set()
        Diction[line[j][:-1]].add(line[0])
    if line[-1] not in Diction:
        Diction[line[-1]] = set()
    Diction[line[-1]].add(line[0])
Diction = sorted(list(Diction.items()))
print(len(Diction), file=ouf)
#for tuple_ in Diction:
print('\n'.join([tuple_[0] + ' - ' + ', '.join(sorted(list(tuple_[1]))) for tuple_ in Diction]), file=ouf)
inf.close()

