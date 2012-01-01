#!/usr/bin/python3
masha=[]
pasha=[]
ansmasha=[]
anspasha=[]
intersect=[]
n, m = list(map(int, input().split()))
for a in range(n):
    masha.append(int(input()))
for a in range(m):
    pasha.append(int(input()))
masha.sort()
pasha.sort()
i=0
j=0
while(i < n and j < m):
    if(masha[i] < pasha[j]):
        ansmasha.append(masha[i])
        i+=1
    elif(masha[i] > pasha[j]):
        anspasha.append(pasha[j])
        j+=1
    elif(masha[i] == pasha[j]):
        intersect.append(masha[i])
        i+=1
        j+=1
for a in range(i, n):
    ansmasha.append(masha[a])
for a in range(j, m):
    anspasha.append(pasha[a])
print(str(len(intersect)) + " " + " ".join(list(map(str, intersect))))
print(str(len(ansmasha)) + " " + " ".join(list(map(str, ansmasha))))
print(str(len(anspasha)) + " " + " ".join(list(map(str, anspasha))))
