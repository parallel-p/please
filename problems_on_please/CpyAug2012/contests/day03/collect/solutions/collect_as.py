#python3
v = list(map(int, input().split()))
q = list(map(int, input().split()))

for i in q:
	l = -1
	r = len(v)
	while (l < r - 1):
		m = (l + r) / 2
		if (v[m] <= i):
			l = m
		else:
			r = m
	if (l == -1) or (v[l] != i):
		print("NO")
	else:
		print("YES")

