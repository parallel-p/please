#python3
n = int(input())

s = []

d = 2
while d * d <= n:
  if n % d == 0:
    s.append(d)
    n //= d
  else:
    d += 1

s.append(n)
print(s)

