#!/usr/bin/python3
import sys

fin = open("priority-queue.in", "r")
fout = open("priority-queue.out", "w")

Priority = {}
Priorities = {}
for cmd in fin.readlines():
    cmd = cmd.rstrip().split()
    if cmd[0] == "ADD":
        cmd[2] = int(cmd[2])
        Priority[cmd[1]] = cmd[2]
        if cmd[2] not in Priorities:
            Priorities[cmd[2]] = set()
        Priorities[cmd[2]].add(cmd[1])
    elif cmd[0] == "POP":
        max_priority = max(Priorities.keys())
        max_id = Priorities[max_priority].pop()
        print(max_id, max_priority, file=fout)
        del Priority[max_id]
        if len(Priorities[max_priority]) == 0:
            del Priorities[max_priority]
    else:
        cmd[2] = int(cmd[2])
        Priorities[Priority[cmd[1]]].discard(cmd[1])
        if len(Priorities[Priority[cmd[1]]]) == 0:
            del Priorities[Priority[cmd[1]]]
        if cmd[2] not in Priorities:
            Priorities[cmd[2]] = set()
        Priorities[cmd[2]].add(cmd[1])
        Priority[cmd[1]] = cmd[2]
fin.close()
fout.close()
