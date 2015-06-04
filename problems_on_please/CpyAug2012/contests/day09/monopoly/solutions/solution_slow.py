#!/usr/bin/python3
import bisect

List = list(map(int, open('monopoly.in', 'r').read().strip().split()))
Answer = 0
for i in range(len(List)):
    List[i] = -List[i]
List.sort()
while len(List) != 1:
    min1 = List.pop()
    min2 = List.pop()
    sum = min1 + min2
    Answer += sum
    List.insert(bisect.bisect_right(List, sum), sum)
print(round(-Answer * 0.05, 2), file=open('monopoly.out', 'w'))

