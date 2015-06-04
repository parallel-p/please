#python3
k = int(input())
a = []
s = input().split(" ")
for i in s:
    a.append(int(i))
a.sort()
print(a[len(a)-k])