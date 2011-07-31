input  = open("keyvalue.in", "r")
output = open("keyvalue.out", "w")

number = int(input.readline())

for i in range(0, number - 1):
	input.readline()

output.write(input.readline().replace("key" + str(number) + " = ", ""))

#for jj in range(0, 1000000000):
	#bk = jj*jj

input.close()
output.close()