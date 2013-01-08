#!/usr/bin/python3
import sys

def SiftUp(Heap, idx, Priority, BackLinks):
    val = Heap[idx]
    while idx > 1 and Priority[Heap[idx // 2]] < Priority[val]:
        Heap[idx] = Heap[idx // 2]
        BackLinks[Heap[idx]] = idx
        idx //= 2
    Heap[idx] = val
    BackLinks[val] = idx


def SiftDown(Heap, idx, Priority, BackLinks):
    while 2 * idx < len(Heap):
        min_child = idx
        if Priority[Heap[2 * idx]] > Priority[Heap[min_child]]:
            min_child = 2 * idx
        if 2 * idx + 1 < len(Heap) and Priority[Heap[2 * idx + 1]] > Priority[Heap[min_child]]:
            min_child = 2 * idx + 1
        if min_child == idx:
            return
        else:
            Heap[min_child], Heap[idx] = Heap[idx], Heap[min_child]
            BackLinks[Heap[idx]] = idx
            BackLinks[Heap[min_child]] = min_child
            idx = min_child


def Add(Heap, elem, priority, Priority, BackLinks):
    Heap.append(elem)
    Priority[elem] = priority
    BackLinks[elem] = len(Heap) - 1
    SiftUp(Heap, len(Heap) - 1, Priority, BackLinks)

def Pop(Heap, Priority, BackLinks):
    id = Heap[1]
    res = id, Priority[id]
    Heap[1] = Heap[-1]
    BackLinks[Heap[1]] = 1
    Heap.pop()
    del Priority[id]
    del BackLinks[id]
    SiftDown(Heap, 1, Priority, BackLinks)
    return res

def Change(Heap, id, priority, Priority, BackLinks):
    old_priority = Priority[id]
    Priority[id] = priority
    if priority > old_priority:
        SiftUp(Heap, BackLinks[id], Priority, BackLinks)
    elif priority < old_priority:
        SiftDown(Heap, BackLinks[id], Priority, BackLinks)


def Len(Heap):
    return len(Heap) - 1

fin = open("priority-queue.in", "r")
fout = open("priority-queue.out", "w")

Queue = ['@']
Priority = {}
BackLinks = {}
for cmd in fin.readlines():
    cmd = cmd.rstrip().split()
    if cmd[0] == "ADD":
        Add(Queue, cmd[1], int(cmd[2]), Priority, BackLinks)
    elif cmd[0] == "POP":
        id, priority = Pop(Queue, Priority, BackLinks)
        print(id, priority, file=fout)
    else:
        Change(Queue, cmd[1], int(cmd[2]),Priority, BackLinks)
fin.close()
fout.close()
