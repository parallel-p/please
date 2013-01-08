#!/dev/python3

A = list(map(int, input().split()))

for x in map(int, input().split()):
    l = -1
    r = len(A)

    while r - l > 1:
        m = (l + r) // 2
        if A[m] >= x:
            r = m
        else:
            l = m
    lb = r
    l = -1
    r = len(A)
    while r - l > 1:
        m = (l + r) // 2
        if A[m] > x:
            r = m
        else:
            l = m
    ub = r
    print(ub - lb)

