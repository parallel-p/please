#!/usr/bin/python3
#!/usr/bin/python3
from io import *
inf = open(file = 'frequency.in', mode = 'r')
ouf = open(file = 'frequency.out', mode = 'w')
now = inf.readline()
Diction = {}
while now:
    now = now.split()
    for word in now:
        if word in Diction:
            Diction[word] += 1
        else:
            Diction[word] = 1
    now = inf.readline()
Diction = list(Diction.items())
for i in range(len(Diction)):
    Diction[i] = [Diction[i][1], Diction[i][0]]
Diction.sort()
for i in range(len(Diction)):
    print(Diction[i][1], file=ouf)


inf.close()
