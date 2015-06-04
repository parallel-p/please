f = open("pants.in", "r")
lines = f.readlines()
f.close()
n = int(lines[0])

s = set(lines[1].split())

g = open("pants.out", "w")
g.write(str(len(s)))
g.close()
