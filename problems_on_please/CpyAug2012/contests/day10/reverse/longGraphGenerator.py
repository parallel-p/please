#python3
import random
import sys

if len(sys.argv) > 1:
    random.seed(sys.argv[1])

n = 50000;
print(n)

m = 50000
for i in range(m):
    a = random.randint(1, n)
    b = a
    while (a == b):
        b = random.randint(1, n)
    print(a, b)

