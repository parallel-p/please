#python3
fin = open('numbers.in')
fout = open('numbers.out', 'w')

n = int(fin.readline())

count = [[0]*12 for i in range(n)]

for i in range(2, 11):
    count[0][i] = 1
    
for i in range(1, n):
    for j in range(1, 11):
        count[i][j] = count[i - 1][j - 1] + count[i - 1][j] + count[i - 1][j + 1]

answer = 0        
for i in range(1, 11):
    answer += count[n-1][i]

print(answer, file=fout)

fin.close()
fout.close()