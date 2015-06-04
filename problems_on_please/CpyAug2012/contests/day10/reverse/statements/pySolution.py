#python3
fin = open("reverse.in", "r")
fout = open("reverse.out", "w")

n = int(fin.readline())

graph = [[] for i in range(n)]

for i in range(n):
    tmp = fin.readline().split()
    for j in tmp:
        graph[int(j)].append(i)
        
for i in graph:
    for j in graph[i]:
        print(j)