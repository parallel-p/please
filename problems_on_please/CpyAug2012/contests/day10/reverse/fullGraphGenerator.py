#python3
import random
import sys

if len(sys.argv) > 1:
    random.seed(sys.argv[1])

n = 500;
print(n)

for i in range(n):
    for j in range(n):
        print(j + 1, end=' ' if j < n - 1 else '\n')
    
