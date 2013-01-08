inf = open("floyd.in", "r")
n = int(inf.readline())

d = []
for i in range(n):
	d.append([int(x) for x in inf.readline().split()])

for k in range(n):
	for i in range(n):
		for j in range(n):
			if d[i][j] > d[i][k] + d[k][j]:
				d[i][j] = d[i][k] + d[k][j]

ouf = open("floyd.out", "w")
for i in range(n):
	ouf.write(" ".join(list(map(str, d[i]))) + "\n")