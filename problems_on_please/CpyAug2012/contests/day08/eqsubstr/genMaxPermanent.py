#python3
import random
import sys
import string


def randString(n):
    a = string.ascii_letters
    return ''.join(['a' for i in range(n)])


def randSegment():
    l = random.randint(SLen // 2, SLen)
    a = random.randint(1, SLen - l + 1)
    b = a + l - 1
    return a, b


if len(sys.argv) > 1:
    random.seed(sys.argv[1])
    
SLen = 100000;
s = randString(SLen)
print(s)

n = 49999;
print(n)

for i in range(SLen):
    print(*randSegment(), end=" ")
    print(*randSegment())
    
    
