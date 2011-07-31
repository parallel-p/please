import random
import string
import sys
#print("TEST ARG:" + sys.argv[1])
if len(sys.argv) > 1:
	random.seed(sys.argv[1])

def random_stringg():
	return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(random.randint(5, 100)))
	

	print(sys.argv[1], "!")

max = random.randint(0, 1000)
print(max - 1)
for i in range(1, max):
	random_string1 = random_stringg()
	if i == max - 1:
		answer = random_string1	
											
	print("key" + str(i) + " = " + random_string1)
				