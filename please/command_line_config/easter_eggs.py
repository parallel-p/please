from please.command_line.template import Template
import sys
import time

def take_over_the_world():
    sys.stdout.write("In progress.")
    while True:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)

def add_easter_eggs_operations(matcher):
    matcher.add_handler(
        Template("take over the world".split()),
        take_over_the_world,
        True)
    matcher.add_handler(
        Template("say @words".split()),
        lambda words: print(" ".join(words)),
        True)
    matcher.add_handler(
        Template("make me @food".split()),
        lambda food: print("Try: sudo make me " + " ".join(food)),
        True)


