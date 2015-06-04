max_num = 1001
EPS = 0.00000001

def equation(x):
    global a, b, c, d
    return a * (a * x ** 3 + b * x ** 2 + c * x + d)

def search_root():
    left = -float(max_num)
    right = float(max_num)
    x = 0
    while right - left > EPS :
        x = (right + left) / 2
        #print(left, eqantion(x), right)
        if equation(x) > 0:
            right = x
        else :
            left = x
    return (left + right) / 2
    
    
a, b, c, d = tuple(map(int, input().split()))
print(search_root())