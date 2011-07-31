#!/usr/bin/python3
fr = open("access.in", "r")
fw = open("access.out", "w")

rights = {}
num = int(fr.readline())
for i in range(num):
    line = fr.readline().split()
    rights[line[0]] = line[1:]
num = int(fr.readline())
for line in fr.readlines():
    line = line.split()
    if line[0][0] == 'r':
        if "R" in rights[line[1]]:
            fw.write("OK\n")
        else: fw.write("Access denied\n")
    elif line[0][0] == 'w':
        if "W" in rights[line[1]]:
            fw.write("OK\n")
        else: fw.write("Access denied\n")
    elif line[0][0] == 'e':
        if "X" in rights[line[1]]:
            fw.write("OK\n")
        else: fw.write("Access denied\n")
    

    
