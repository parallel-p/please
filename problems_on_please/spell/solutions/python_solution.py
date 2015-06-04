a = set()
with open("spell.in", "r") as fp:
    s = str(fp.readline()).strip("\n")
    for word in s.split(" "):
        if(word != ""):
            a.add(word)
ans = len(a)
with open("spell.out", "w") as out:
    out.write(str(ans))

