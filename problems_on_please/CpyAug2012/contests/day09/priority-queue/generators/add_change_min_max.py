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

Prior = set()
Names = set()
Lmin = []
Lmax = []
for i in range(N // 6):
    id = RandomName()
    while id in Names:
        id = RandomName()
    prior = 1 + i
    print("ADD", id, prior)
    Names.add(id)
    Lmin.append(id)
    Prior.add(prior)

    id = RandomName()
    while id in Names:
        id = RandomName()
    prior = 10 ** 9 - i
    print("ADD", id, prior)
    Names.add(id)
    Lmax.append(id)
    Prior.add(prior)

for i in range(N // 6):
    prior = random.randint(5 * 10 ** 8, 9 * 10 ** 8)
    while prior in Prior:
        prior = random.randint(5 * 10 ** 8, 9 * 10 ** 8)
    print("CHANGE", Lmin[i], prior)
    Prior.add(prior)

    prior = random.randint(1 * 10 ** 8, 5 * 10 ** 8)
    while prior in Prior:
        prior = random.randint(5 * 10 ** 8, 9 * 10 ** 8)
    print("CHANGE", Lmax[i], prior)
    Prior.add(prior)

for i in range(N // 6 * 2):
    print("POP")
