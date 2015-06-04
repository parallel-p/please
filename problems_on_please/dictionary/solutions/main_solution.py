#/usr/bin/python3
d = {}
numbers = input()
for i in range (int(numbers)):
    our_key = input()
    our_value = input()
    d[our_key] = our_value
    d[our_value] = our_key

to_translate = input()
print (d[to_translate])
    
