#!/usr/bin/python3

inf = open('priority-queue.in', 'r')
ouf = open('priority-queue.out', 'w')

H = [None]

pos = {}

def swap(a, b):
    H[a], H[b] = H[b], H[a]
    pos[H[a][1]] = a
    pos[H[b][1]] = b

def sift_up(v):
    while (v != 1):
        if (H[v // 2] > H[v]):
            break
        else:
            swap(v // 2, v)
            v = v // 2

def add(elem, prior):
    pos[elem] = len(H)
    H.append((prior, elem))
    sift_up(len(H) - 1)

def sift_down(v):
    while (2 * v < len(H)):
        ind = 2 * v
        if 2 * v + 1 < len(H) and H[2 * v + 1] > H[2 * v]:
            ind = 2 * v + 1
        if (H[ind] < H[v]):
            break
        swap(v, ind)
        v = ind

def extract_min():
    assert len(H) > 1
    swap(1, len(H) - 1)
    del pos[H[-1][1]]
    ret = H.pop()
    sift_down(1)
    return ret[1], ret[0]

for command in inf.readlines():
    command = command.strip().split()
    if (command[0] == 'ADD'):
        add(command[1], int(command[2]))
    elif (command[0] == 'POP'):
        print(*extract_min(), file=ouf)
    else:
        H[pos[command[1]]] = (int(command[2]), command[1])
        sift_up(pos[command[1]])
        sift_down(pos[command[1]])
