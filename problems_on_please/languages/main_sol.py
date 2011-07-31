n = int(input())

d = {}

for i in range(n):
    m = int(input())
    for j in range(m):
        s = str(input())
        d.setdefault(s,0)
        d[s] += 1
        

m = 0
res = []
res2 = []
for i in d.keys():
    res2.append(i)
    if d[i] == n:
        res.append(i)
        
print(len(res))
for i in res:
    print(i)
    
print(len(res2))
for i in res2:
    print(i)
        
        