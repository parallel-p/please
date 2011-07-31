#gen.py words_count unique_words_count max_word_len [random_ini]

import sys
import random

word_symbols = r'abcdefghijklmnopqrstuvwxyz'
new_line_prob = 0.1

def gen_word(maxlen):
    s = ""
    l = random.randint(1, maxlen)
    for i in range(l):
        s += random.choice(word_symbols)
    return s
    
def gen_list(listlen, maxwordlen):
    l = set()
    while len(l) != listlen:
        l.add(gen_word(maxwordlen))
    l = list(l)
    random.shuffle(l)
    return l
    
words_count, unique_words_count, max_word_len = list(map(int, sys.argv[1:4]))
random_ini = str(words_count) + str(unique_words_count) + str(max_word_len)
if len(sys.argv) > 4:
    random_ini += sys.argv[4]
random.seed(random_ini)
list = gen_list(unique_words_count, max_word_len)
ans = list
for i in range(words_count - unique_words_count):
    ans.append(random.choice(list))
    
list = []
for i in ans:
    list.append(i)
    if random.random() <= new_line_prob:
        s = ''
        for i in list:
            s += i + ' '
        print(s[:-1])
        list = []
s = ''
for i in list:
    s += i + ' '
print(s[:-1])