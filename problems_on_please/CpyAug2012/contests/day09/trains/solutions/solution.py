#!/usr/bin/python3
from sys import stdin, exit

H = [None]

def sift_up(v):
    while (v != 1 and H[v // 2] > H[v]):
        H[v], H[v // 2] = H[v // 2], H[v]

def sift_down(v):
    while 2 * v < len(H):
        cp = 2 * v
        if cp + 1 < len(H) and H[cp + 1] < H[cp]:
            cp = cp + 1
        if H[cp] > H[v]:
            break
        H[cp], H[v] = H[v], H[cp]
    
def extract_min():
    if len(H) == 1:
        return None
    ret = H[1]
    H[1], H[-1] = H[-1], H[1]
    H.pop()
    sift_down(1)
    return ret

def add(x):
    H.append(x)
    sift_up(len(H) - 1)

L = open('trains.in', 'r').readlines()
n = int(L[0])

place = {}
for i in range(1, n + 1):
    add(i)

Answer = []


ouf = open('trains.out', 'w')
for f in L[1:]:
    f = f.strip()
    if f[0] == '+':
        place[f[1:]] = extract_min()
        if place[f[1:]] is None:
            print(0, f[1:], file=ouf)
            exit(0)
        Answer.append((f[1:], place[f[1:]]))
    else:
        assert f[1:] in place
        add(place[f[1:]])
ouf.write('\n'.join("%s %s" % x for x in Answer))
        
