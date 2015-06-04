from sys import *
from random import *

N = 100
if len(argv) > 1:
    N = int(argv[1])
A = []
for i in range(N):
    A.append(str(randint(1,N)))
print(" ".join(A))
