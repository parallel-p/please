#/usr/bin/python3

import sys
sys.stdin = open('coins.in')
sys.stdout = open('coins.out', 'w')

n, m = [int(x) for x in input().split()]
a = [int(x) for x in input().split()]
nums = [0] * m
exit = False
a.sort()

def count():
    global m, a, nums
    ans = 0
    i = 0
    while i < m:
        ans += a[i] * nums[i]
        i += 1
    return ans

if sum(a) * 2 < n:
    print(-1)
    exit = True
else:
    i = 0
    while i < 3 ** m:
        if count() == n:
            print(sum(nums))
            j = 0
            while j < m:
                if nums[j] == 2:
                    print(a[j], a[j], end = ' ')
                elif nums[j] == 1:
                    print(a[j], end = ' ')
                j += 1
            exit = True
            break
        else:
            j = 1
            while j < m + 1:
                if nums[-j] == 2:
                    nums[-j] = 0
                else:
                    nums[-j] += 1
                    break
                j += 1
        i += 1
if not exit:
    print(0)
