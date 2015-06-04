#solution1 python3
s = input().split(" ")
a = []
for i in s:
    a.append(int(i))
s = input().split(" ")
splitter = [0]
for i in s:
    splitter.append(int(i))
splitter.append(len(a))

for i in reversed(range(len(splitter) - 1)):
    b = a[splitter[i]:splitter[i + 1]]
    for j in b:
        print(j, end = " ")
print()        
