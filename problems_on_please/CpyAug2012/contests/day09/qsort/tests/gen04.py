#!/usr/bin/python3
from sys import argv
n = int(argv[1]) // 2
print(' '.join(map(str, [2 * i for i in range(n // 2)] + [2 * i - 1 for i in range(n // 2, 0, -1)])))
