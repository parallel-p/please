import sys
dictionary = {}
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
for line in sys.stdin:
    for ch in line:
        if ch in alphabet:
            if not ch in dictionary:
                dictionary[ch] = 0;
            else:
                dictionary[ch]+=1;
best = '\n'
maxnum = 0;
for token in sorted(dictionary):
    if dictionary[token] > maxnum:
        maxnum = dictionary[token]
        best = token
print(best)
    
    