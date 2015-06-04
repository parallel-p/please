#python3
import random
import sys
if len(sys.argv) > 1:
    random.seed(sys.argv[1])
len = 100000;
print(random.randint(1, len+1))
for i in range(len):
    print(random.randint(1, 10**20), end = "\n" if(i == len-1) else " ")