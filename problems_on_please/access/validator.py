#!/usr/bin/python3
import sys
import logging

class ValidationError(Exception):
    pass

operations = ["read", "write", "execute"]

a = int(sys.stdin.readline())
for line in range(a):
    line = sys.stdin.readline()
    if len(line.split()) == 1:
        raise ValidationError("Not found any properties")
b = int(sys.stdin.readline())
for line in range(b):
    line = sys.stdin.readline()
    line = line.split()
    if line[0] not in operations:
        raise ValidationError("Found unavailable operation %s", line[0])