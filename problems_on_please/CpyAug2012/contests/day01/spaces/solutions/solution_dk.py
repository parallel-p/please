#!/usr/bin/python3

S = input()
Ans = ''
for i in range(len(S)):
    if S[i] == '-' and (i == 0 or S[i - 1] != ' '):
        Ans += ' '
    Ans += S[i]
    if S[i] in (".", ",", "?", "!", "-") and i < len(S) - 1 and S[i + 1] != ' ':
        Ans += ' '
print(Ans)

