import os
dir = os.path.split(__file__)[0]
inf = os.path.join(dir, "result.in")
ouf = os.path.join(dir, "result.out")
in_file = open(inf, "r")
out_file = open(ouf, "w")
out_file.write(in_file.read())

    
    
    
