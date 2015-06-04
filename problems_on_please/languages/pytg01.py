import random

num_of_words = 10
lenn = 1
num_of_pep = 10
num_in_pep = 5


words = []
for i in range(num_of_words):
    s = ""
    for j in range(lenn):
        s += chr(random.randint(97,122))
    words.append(s)

print(num_of_pep)

used =[]
for i in range(num_of_words+1):
    used.append(True)
    
for i in range(num_of_pep):
    m = random.randint(1, num_in_pep)
    print(m)
    for j in range(len(used)): 
        used[j] = True   
    k = num_of_words
    used[k] = False
    for j in range(m):       
        while not(used[k]) :
            k = random.randint(0,num_of_words-1)
        print(words[k])
        used[k] = False
    
    
