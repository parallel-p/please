#python3
def dijkstra(x):
    dist[x] = 0
    for i in range(n):
        mn = 9999999999
        iod = -1
        for j in range(n):
            if mn > dist[j] and not used[j]:
                mn = dist[j]
                iod = j
        if iod == -1:
            break
        used[iod] = True
        for v in range(n):
            if iod != v and mas[iod][v] != -1:
                if dist[v] > dist[iod] + mas[iod][v]:
                    dist[v] = dist[iod] + mas[iod][v]

infile = open('dijkstra.in')
n, s, f = map(int, infile.readline().split())
s -= 1
f -= 1
mas = []
for i in range(n):
    mas += [list(map(int, infile.readline().split()))]
dist = [9999999999] * n
out = open('dijkstra.out', 'w')
used = [False] * n
dijkstra(s)
if dist[f] != 9999999999:
    print(dist[f], file = out)
else:
    print(-1, file = out)