import os
dir = os.path.split(__file__)[0]
inf = os.path.join(dir, "result.in")
ouf = os.path.join(dir, "result.out")
with open(inf, "r") as in_file:
    with open(ouf, "w") as out_file: 
        out_file.write(in_file.read())

    
    
    
