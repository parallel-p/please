import sys

words = {}

for line in sys.stdin:
    for x in line.split():
        if not x in words:
            words[x] = 1
        else:
            words[x] += 1
            
words = [(k,v) for k,v in words.items()]
words.sort(key = lambda x: x[0])
words.sort(key = lambda x: x[1], reverse=True)
for x in words:
    print(x[0])
