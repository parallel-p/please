#!/usr/bin/python3
import random
import sys

namespace = []

random.seed(int(sys.argv[5]))

rights = ["W", "R", "X"]
operations = ["read", "write", "execute"]

def gen_file():
    name = 'tmp_' + str(random.randint(0, 1<<30))
    while name in namespace:
        name = 'tmp_' + str(random.randint(0, 1<<30))
    namespace.append(name)
    return name

min_rand_n = int(sys.argv[1])
max_rand_n = int(sys.argv[2])
min_rand_m = int(sys.argv[3])
max_rand_m = int(sys.argv[4])


n = random.randint(min_rand_n, max_rand_n)

print(n)
for i in range(n):
    file = gen_file()
    right = random.sample(rights, random.randint(1,3))
    print(file, *right)
    
m = random.randint(min_rand_m, max_rand_m)
print(m)

for i in range(m):
    print(random.choice(operations), random.choice(namespace))