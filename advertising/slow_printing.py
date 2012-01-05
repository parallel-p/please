import sys
from time import sleep
import random

delay = float(sys.argv[1])
random_delay = float(sys.argv[2])

def delay_choose():
    if random.randint(0, 5) != 0:
        return random.randint(1, random_delay)
    else:
        return random_delay * random.randint(5, 10)

for c in sys.stdin.read():
    sys.stdout.write(c)
    sys.stdout.flush()
    sleep((delay + delay_choose()) / 1000.0)

