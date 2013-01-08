#!/usr/bin/python3

tmp = input().split()
n = int(tmp[0])
k = int(tmp[1])
answer = [0]*n
answer[0] = 1

for i in range(n):
    for j in range(i+1, min(i + k + 1, n)):
        answer[j] += answer[i]
print(answer[n-1])
