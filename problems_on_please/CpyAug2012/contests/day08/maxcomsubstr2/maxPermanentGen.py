#python3
import random
import sys
import string

def randString(n):
    a = string.ascii_letters
    return ''.join(['a' for i in range(n)])


def randSegment(n):
    a = random.randint(1, n + 1);
    b = random.randint(1, n + 1);
    if(a > b):
        a, b = b, a    
    return a, b


if len(sys.argv) > 1:
    random.seed(sys.argv[1])
    
aLen = 29999;
a = randString(aLen)
print(a)
bLen = 29999;
b = randString(bLen)
print(b)