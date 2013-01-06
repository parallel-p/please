#python3
fin = open('topsort.in')
fout = open('topsort.out', 'w')

def read_ints(fin):
    return [int(i) for i in fin.readline().split()]


n, m = read_ints(fin)
in_deg = [0] * n
adj_list = [[] for i in range(n)]

for i in range(m):
    v, w = read_ints(fin)
    v -= 1
    w -= 1
    adj_list[v].append(w)
    in_deg[w] += 1

sources = []
for i in range(n):
    if in_deg[i] == 0:
        sources.append(i)

topological_order = []
while sources:
    v = sources.pop()
    topological_order.append(v)
    for w in adj_list[v]:
        in_deg[w] -= 1
        if in_deg[w] == 0:
            sources.append(w)

if len(topological_order) == n:
    print(' '.join([str(i + 1) for i in topological_order]), file=fout)
else:
    print(-1, file=fout)


fout.close()