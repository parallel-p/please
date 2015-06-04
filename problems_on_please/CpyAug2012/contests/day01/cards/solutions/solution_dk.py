#!/usr/bin/python3
Cards = input().split()
Sep = [0] + list(map(int, input().split())) + [len(Cards)]
Ans = []
for i in range(len(Sep) - 1, 0, -1):
    Ans += Cards[Sep[i - 1]:Sep[i]]
print(" ".join(Ans))


