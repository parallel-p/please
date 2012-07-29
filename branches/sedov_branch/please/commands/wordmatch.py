import difflib

def similarity(list, word):
    s = difflib.SequenceMatcher()
    s.set_seq2(word)
    maxratio = 0
    closest = None
    for element in list:
        s.set_seq1(element)
        if (s.real_quick_ratio() > maxratio and
            s.quick_ratio() > maxratio):
            ratio = s.ratio()
            if ratio > maxratio:
                maxratio = ratio
    return maxratio

def contains(list, word):
    return similarity(list, word) > 0.4

