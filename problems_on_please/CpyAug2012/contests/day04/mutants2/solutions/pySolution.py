#!/usr/bin/python3
class point:
    x = 0
    y = 0


tmp = input().split()
n = int(tmp[0])
m = int(tmp[1])
field = [[0]*m for i in range(n)]
for i in range(n):
    tmp = input().split()
    for j in range(m):
        field[i][j] = int(tmp[j])
answer = [[0]*m for i in range(n)]
way = [[]]

for i in range(n):
    way.append([])
    for j in range(m):
        way[i].append(point())
        
for i in range(n - 1, -1, -1):
    for j in range(m - 1, -1, -1):
        answer[i][j] = field[i][j]
        if i == n - 1 and j == m - 1:
            pass
        elif i == n - 1:
            way[i][j].x = i
            way[i][j].y = j + 1 
            answer[i][j] += answer[i][j + 1]
        elif j == m - 1:
            way[i][j].x = i + 1
            way[i][j].y = j
            answer[i][j] += answer[i + 1][j]            
        elif answer[i + 1][j] < answer[i][j + 1]:
            way[i][j].x = i + 1
            way[i][j].y = j
            answer[i][j] += answer[i + 1][j] 
        else:
            way[i][j].x = i
            way[i][j].y = j + 1 
            answer[i][j] += answer[i][j + 1]


print(answer[0][0])
