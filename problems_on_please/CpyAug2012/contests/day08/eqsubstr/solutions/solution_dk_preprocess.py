#!/usr/bin/python3

fin = open("eqsubstr.in", "r")
fout = open("eqsubstr.out", "w")

POW = 179
MOD = 10 ** 17 + 3
S = fin.readline().rstrip()
n = len(S)
Powers = [1] + [0] * n
PrefixHash = [0] * (n + 1)
for i in range(1, n + 1):
    Powers[i] = Powers[i - 1] * POW % MOD
    PrefixHash[i] = (PrefixHash[i - 1] * POW + ord(S[i - 1])) % MOD

def Hash(S, i, j): # Hash of S[a:b]
    return (PrefixHash[j] - PrefixHash[i] * Powers[j - i]) % MOD

NQueries = int(fin.readline().rstrip())
if n <= 100:
  for i in range(NQueries):
    l1, r1, l2, r2 = map(int, fin.readline().rstrip().split())
    if Hash(S, l1 - 1, r1) == Hash(S, l2 -1, r2):
        fout.write("+")
    else:
        fout.write("-")
fout.write("\n")
fin.close()
fout.close()



