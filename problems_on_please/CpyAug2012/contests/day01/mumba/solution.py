#python3
from re import search
print("NO" if search(r"(?:b{2}|([a-z]+?)\1{2})",input())!=None else "YES")