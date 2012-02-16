import difflib

CUTOFF = 0.4
def similarity(list, word):
    s = difflib.SequenceMatcher()
    s.set_seq2(word)
    maxratio = CUTOFF
    closest = None
    for element in list:
        s.set_seq1(element)
        if (s.real_quick_ratio() > CUTOFF and
            s.quick_ratio() > CUTOFF and
            s.ratio() > CUTOFF):
            break
    else:
        return 0
    return s.ratio()

def contains(list, word):
    return similarity(list, word) > 0

