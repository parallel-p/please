#!/dev/python3

n, k = map(int, input().split())

L = list(map(int, input().split()))

def get(l):
    return sum(x // l for x in L)

a, b = 0, sum(L)
while (b - a > 1):
    mid = (a + b) // 2
    if (get(mid) >= k):
        a = mid
    else:
        b = mid

print(a)
        
