import difflib

CUTOFF = 0.6
def contains(list, word):
    s = difflib.SequenceMatcher()
    s.set_seq1(word)
    maxratio = CUTOFF
    closest = None
    for element in list:
        s.set_seq2(word)
        if (s.real_quick_ratio() > CUTOFF and
            s.quick_ratio() > CUTOFF and
            s.ratio() > CUTOFF):
            break
    else:
        return False
    return True

