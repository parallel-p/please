#!/usr/bin/env python3
cost = {}
for letter_index in range(26):
    cost[chr(ord('a') + letter_index)] = int(input())
s = input()
sum = 0
for letter in s:
    sum += cost[letter]
print(sum)
