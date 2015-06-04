dic = set()
ans = 0
with open("inside.in", 'r') as inf:
    i = 0
    for line in inf:
        s = line.strip()
        if (i % 2 == 0):
            i += 1
            continue
        if (i == 1):
            for num in s.split(" "):
                dic.add(num)                
        if (i == 3):
            for num in s.split(" "):
                if (num in dic):
                    ans += 1
        i += 1

with open("inside.out", 'w') as ouf:
    ouf.write(str(ans))
