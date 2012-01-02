import psutil
import sys

MEGABYTE = 1 << 20
p = psutil.Popen(["test.exe", '0.1', sys.argv[1]])
#print(p.get_memory_info())
while (p.is_running()):
	print(str(p.get_memory_info()[0] / MEGABYTE)+' '+str(p.get_memory_info()[1] / MEGABYTE))
	try:
		p.wait(0.01)
	except:
		pass
