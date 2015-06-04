import random

def random_string () :
    months = {1:"JAN", 2:"FEB", 3:"MAR", 4:"APR", 5:"MAY", 6:"JUN", 7:"JUL", 8:"AUG", 9:"SEP", 10:"OCT", 11:"NOV", 12:"DEC"}
    a = random.randint(1, 12)
    return months[a]

def random_day ():
    return random.randint(1, 31)

def random_year ():
    return random.randint(0, 99)

def main ():
    fin = open ('date_decoder.in','w')
    fout = open ('date_decoder.out','w')
    
    fin.write(str(random_day()) + '-' + random_string() + '-' + str(random_year))
    print(str(random_day()) + '-' + random_string() + '-' + str(random_year()))
    
    fin.close()
    fout.close()
    
    
if __name__ == "__main__" :
    main()