import random
import string

def random_string () :
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(3, 10))

def main ():
    print(str(random_string()) + ' ' + str(random.randint(0, 100)))
    
if __name__ == "__main__" :
    main()