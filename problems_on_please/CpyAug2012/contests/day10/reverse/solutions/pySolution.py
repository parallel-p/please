#python3
fin = open("reverse.in", "r")
fout = open("reverse.out", "w")

n = int(fin.readline())
fout.write(str(n) + "\n")

graph = [[] for i in range(n)]

for i in range(n):
    tmp = fin.readline().split()
    for j in tmp:
        graph[int(j) - 1].append(i)
        
for i in graph:
    for j in i:
        fout.write(str(j + 1))
        fout.write(" ")
    fout.write("\n")
