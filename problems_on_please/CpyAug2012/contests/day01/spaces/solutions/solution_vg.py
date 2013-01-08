#python3
s = list(input())
prev = ""
for ch in s:
    if ch == '-':
        if prev != ' ':
            print(' ', end="")
    if ch == ' ':
        print(ch, end="")
    elif prev in ['-', '.', ',', '!', '?']:
        print(' ' + ch, end="")
    else:
        print(ch, end="")
    prev = ch
print()