from please.command_line.template import Template
import sys
import time

import random

def take_over_the_world():
    sys.stdout.write("In progress.")
    while True:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)

def sudo_make_me_food(food):
    if food != ['sandwich']:
        print('Sorry, doesn\'t know how to make', *food)
    else:
        print('Okay.', 'http://xkcd.com/149/')

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
    matcher.add_handler(
        Template(["sudo", "make", "me", "@food"]),
                 sudo_make_me_food,
                 True)
    matcher.add_handler(
        Template(["smile"]),
        lambda: print(random.Random().choice([":-)", "(^ ^)", ":-D"])),
        True)


