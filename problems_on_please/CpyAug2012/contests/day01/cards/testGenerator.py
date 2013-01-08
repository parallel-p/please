#python3
import random
import sys
if len(sys.argv) > 1:
    random.seed(sys.argv[1])
len = random.randint(1,100000);
for i in range(len):
    print(random.randint(-100000, 100000), end = "\n" if i == len - 1 else " ")
s = ""
for i in range(1, len):
    if random.randint(0,3) or i == 2:
        s += str(i) + " "
s = s.strip()
print(s)
