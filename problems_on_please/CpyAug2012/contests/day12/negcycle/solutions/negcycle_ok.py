#python3
import sys

MAXN = 100
INF = 1000000000;
SMALLINF = 100000;

a = [[0] * MAXN for i in range(MAXN)]
next = [[0] * MAXN for i in range(MAXN)];
used = [False] * MAXN;
ans = [];

sys.stdin = open("negcycle.in", "r");
sys.stdout = open("negcycle.out", "w");

n = int(input());

for i in range(n):
        a[i] = list(map(int, input().split()))
        for j in range(n):
                if a[i][j] == SMALLINF:
                         a[i][j] = INF
                next[i][j] = j

for k in range(n):
           for i in range(n):
                     for j in range(n):
                            if a[i][j] > a[i][k] + a[k][j]:
                                a[i][j] = a[i][k] + a[k][j]
                                next[i][j] = next[i][k]

for i in range(n):
          if a[i][i] < 0:
                k = i
                used[i] = True

                while not used[next[k][i]]:
                        k = next[k][i]
                        used[k] = True

                l = next[k][k];
                ans.append(k);
                while l != k:
                        ans.append(l);
                        l = next[l][k];

                print("YES");
                print(len(ans));
                for i in ans:
                        print(i + 1, end=" ");
                print("");
                exit(0);

print("NO");
