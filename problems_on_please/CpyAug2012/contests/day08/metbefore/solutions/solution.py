#!/usr/bin/python3
fin = open('metbefore.in', 'r')
fout = open('metbefore.out', 'w')

A = set()
for i in map(int,fin.readline().strip().split()):
    if i in A:
        print("YES", file=fout)
    else:
        print("NO", file=fout)
        A.add(i)
