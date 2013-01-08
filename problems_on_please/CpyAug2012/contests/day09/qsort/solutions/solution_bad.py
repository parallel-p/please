#!/usr/bin/python3
print(' '.join(map(str, sorted(map(int, open('qsort.in', 'r').read().strip().split())))), file=open('qsort.out', 'w'))
