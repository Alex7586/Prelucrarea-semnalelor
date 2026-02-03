import numpy as np

def findMatch(s, t, MIN_MATCH = 3):
    if len(t) < MIN_MATCH:
        return (0,0,t[0] if t is not None else None)
    
    pos = s.rfind(t[:MIN_MATCH])
    if pos == -1:
        return (0, 0, t[0])

    best_len = MIN_MATCH
    best_pos = pos

    l = MIN_MATCH + 1
    while l <= len(t):
        pos2 = s.rfind(t[:l])
        if pos2 == -1:
            break
        best_len = l
        best_pos = pos2
        l += 1

    d = len(s) - best_pos
    c = t[best_len] if best_len < len(t) else None
    return (d, best_len, c)

def outputToEntry(dict, output):
    entry = ''
    index, token = output
    if index is not None:
        entry = outputToEntry(dict, dict[index]) + token
    return entry

def to_matrix(results_dict_for_m, windowLengths, searchBufferProcents):
    # results_dict_for_m[W] = list pe procente
    return np.array([results_dict_for_m[W] for W in windowLengths], dtype=float)


