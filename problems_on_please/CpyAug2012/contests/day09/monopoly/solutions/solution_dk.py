#!/usr/bin/python3

def SiftUp(Heap, idx):
    val = Heap[idx]
    while idx > 1 and Heap[idx // 2] > Heap[idx]:
        Heap[idx] = Heap[idx // 2]
        idx //= 2
    Heap[idx] = val


def SiftDown(Heap, idx):
    while 2 * idx < len(Heap):
        min_child = idx
        if Heap[2 * idx] < Heap[min_child]:
            min_child = 2 * idx
        if 2 * idx + 1 < len(Heap) and Heap[2 * idx + 1] < Heap[min_child]:
            min_child = 2 * idx + 1
        if min_child == idx:
            return
        else:
            Heap[min_child], Heap[idx] = Heap[idx], Heap[min_child]
            idx = min_child


def Add(Heap, elem):
    Heap.append(elem)
    SiftUp(Heap, len(Heap) - 1)


def Pop(Heap):
    res = Heap[1]
    Heap[1] = Heap[-1]
    Heap.pop()
    SiftDown(Heap, 1)
    return res


def Heapify(List):
    Heap = ['@'] + List
    for i in range(len(Heap) // 2, 0, -1):
        SiftDown(Heap, i)
    return Heap


def Len(Heap):
    return len(Heap) - 1


List = list(map(int, open('monopoly.in', 'r').read().strip().split()))
Heap = Heapify(List)
Answer = 0
while Len(Heap) != 1:
    min1 = Pop(Heap)
    min2 = Pop(Heap)
    Answer += min1 + min2
    Add(Heap, min1 + min2)
print(round(Answer * 0.05, 2), file=open('monopoly.out', 'w'))

