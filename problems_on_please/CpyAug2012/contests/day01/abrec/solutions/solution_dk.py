#!/usr/bin/python3

def gen(a, b):
    if a < b:
        gen(a, b - 1)
    print(b, end = ' ')

a, b = map(int, input().split())
gen(a, b)
print()
