#!/usr/bin/python3
#!/usr/bin/python3

fin = open('comb1.in', 'r')
fout = open('comb1.out', 'w')

def gen(n, k, prefix):
    if n == 0:
        print(" ".join(map(str, prefix)), file=fout)
        return
    if k < n:
        gen(n - 1, k, prefix + [0])
    if k > 0:
        gen(n - 1, k - 1, prefix + [1])


n, k = map(int, fin.read().strip().split())
gen(n, k, [])

