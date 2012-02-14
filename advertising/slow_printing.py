import sys
from time import sleep
import random

delay = float(sys.argv[1])
random_delay = float(sys.argv[2])

def delay_choose():
    if random.randint(0, 15) != 0:
        return random.randint(1, random_delay)
    else:
        return random_delay * random.randint(2, 5)

while True:
    buffer = sys.stdin.read(1024)
    if not buffer:
        break
    for c in buffer:
        sys.stdout.write(c)
        sys.stdout.flush()
        sleep((delay + delay_choose()) / 100000.0)

