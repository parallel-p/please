#python3
from bisect import bisect_left, bisect_right

a = list(map(int, input().split()))
for i in map(int, input().split()):
    print(bisect_right(a, i) - bisect_left(a, i))
