#python3
a = list(map(int, input().split()))
b = list(map(int, input().split()))
for i in b:
    l = 0
    r = len(a)
    while l + 1 < r:
        mid = (l + r + 1) // 2
        if a[mid] <= i:
            l = mid
        else:
            r = mid
    print('YES' if a[l] == i else 'NO')

