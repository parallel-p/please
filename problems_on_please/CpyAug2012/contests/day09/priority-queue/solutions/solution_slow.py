#!/usr/bin/python3
import sys

fin = open("priority-queue.in", "r")
fout = open("priority-queue.out", "w")

Priority = {}
for cmd in fin.readlines():
    cmd = cmd.rstrip().split()
    if cmd[0] == "ADD":
        Priority[cmd[1]] = int(cmd[2])
    elif cmd[0] == "POP":
        max_priority = -10 ** 10
        max_id = ""
        for id, priority in Priority.items():
            if priority > max_priority:
                max_priority = priority
                max_id = id
        print(max_id, max_priority, file=fout)
        del Priority[max_id]
    else:
        Priority[cmd[1]] = int(cmd[2])
fin.close()
fout.close()
