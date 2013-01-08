#python3
t = input()
a = [0] * 26
for i in t:
    a[ord(i) - 65] += 1
        
        
l = ''
m = ''
r = ''

#print (a)
for i in range (len (a)):
    while a[i] >= 2:
        l += chr (i + 65)
        r = chr (i + 65) + r
        a[i] -= 2
flag = 0
for i in range (len (a)):
    if flag == 0 and a[i] == 1:
        m = chr (i + 65)
        flag = 1
        
print (l + m + r)
