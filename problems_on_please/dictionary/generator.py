import os
import random
import string
import sys

random.seed(sys.argv[1])
numbers = random.randint(1, 10000)
print(str(numbers))
ololo = ""
e = random.randint(0, numbers -1)
for i in range(numbers):
    if i == e:
        ololo = (''.join(random.choice(string.ascii_uppercase + string.digits)
        for x in range(random.randint(10,15))))
        print(ololo)
    else:
        print(''.join(random.choice(string.ascii_uppercase + string.digits) 
                for x in range(random.randint(10,15))))

    print(''.join(random.choice(string.ascii_uppercase + string.digits) 
            for x in range(random.randint(10,15))))

print(ololo)

