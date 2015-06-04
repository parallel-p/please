#python3
import sys
sys.stdin = open('monopoly.in')
sys.stdout = open('monopoly.out', 'w')


def walk_up(i):
    if heap[i // 2] > heap[i]:
        heap[i], heap[i // 2] = heap[i // 2], heap[i]



def walk_down(position):
    while 2 * position < len(heap):
        index = 2 * position
        if 2 * position + 1 < len(heap) and heap[2 * position + 1] < heap[2 * position]:
            index = 2 * position + 1
        if heap[position] > heap[index]:
            heap[position], heap[index] = heap[index], heap[position]
            position = index
        else:
            return


def del_min():
    heap[1] = heap[-1]
    heap.pop()
    walk_down(1)


def add(elem):
    heap.append(elem)
    walk_up(len(heap) - 1)


heap = list(map(int, input().split()))
heap = sorted(heap)
heap = [0] + heap
n = len(heap)
ans = 0
for i in range(n - 2):
    new = heap[1]
    del_min()
    new = new + heap[1]
    del_min()
    ans = ans + new * 0.05
    add(new)
print(ans)
