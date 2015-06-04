#python3
import random
import sys
import string


def randString(n):
    a = string.ascii_lowercase
    return ''.join([random.choice(a) for i in range(n)])


def randSegment(n):
    a = random.randint(1, n);
    b = random.randint(1, n);
    if a > b:
        a, b = b, a    
    return a, b


if len(sys.argv) > 1:
    random.seed(sys.argv[1])
    
SLen = random.randint(1, 100000);
s = randString(SLen)
print(s)

n = random.randint(1, 100000);
print(n)

for i in range(n):
    print(*randSegment(SLen), end=" ")
    print(*randSegment(SLen))
    