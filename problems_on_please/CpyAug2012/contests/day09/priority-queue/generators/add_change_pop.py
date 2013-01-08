#!/usr/bin/python3

import sys
import random
import string

N = 10

if len(sys.argv) > 1:
    N = int(sys.argv[1])
if len(sys.argv) > 2:
    random.seed(int(sys.argv[2]))

def RandomName(l = 5):
    ans = ""
    while l > 0:
        ans += random.choice(string.ascii_lowercase)
        l -= 1
    return ans

Names = dict()
Prior = set()
for i in range(N // 3):
    id = RandomName()
    while id in Names:
        id = RandomName()
    prior = random.randint(1, 10 ** 9)
    while prior in Prior:
        prior = random.randint(1, 10 ** 9)
    print("ADD", id, prior)
    Names[id] = prior
    Prior.add(prior)
Names_list = list(Names.keys())
for i in range(N // 3):
    id = random.choice(Names_list)
    prior = random.randint(1, 10 ** 9)
    while prior in Prior:
        prior = random.randint(1, 10 ** 9)
    print("CHANGE", id, prior)
    Names[id] = prior
    Prior.add(prior)
for i in range(N // 3):
    print("POP")
