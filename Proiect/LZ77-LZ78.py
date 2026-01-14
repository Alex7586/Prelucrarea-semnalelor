MAX_MATCH = 258
MIN_MATCH = 3

def findMatch(s: bytes, t: bytes):
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

def LZ77_encode(file):
    windowLength = 32768
    search_buffer = int(29/32 * windowLength)
    look_ahead_buffer = windowLength - search_buffer
    output = []
    f = open(file, "rb")
    window = bytearray()
    input = f.read(look_ahead_buffer)
    while input:
        d, l, c = findMatch(window, input)
        output.append((d,l,c))
        
        consume = l + 1 if c is not None else l
        window.extend(input[:consume])
        if len(window) > search_buffer:
            del window[:-search_buffer]
        input = input[consume:] + f.read(consume)

    f.close()
    return output

def LZ77_decode(code):
    result = ''
    for (d,l,c) in code:
        if d != 0:
            result += result[len(result)-d : len(result)-d+l]
        result += c if c is not None else ''
    return result

def outputToEntry(dict, output):
    entry = ''
    index, token = output
    if index is not None:
        entry = outputToEntry(dict, dict[index]) + token
    return entry

def LZ78_encode(file):
    input += '$'
    tree = {}
    index = 1
    output = [(None, '')]
    i = 0
    while i < len(input):
        parent = 0
        while tree.get(parent):
            for child, token in tree[parent]:
                if token == input[i]:
                    parent = child
                    i += 1
                    break
            else:
                tree[parent].append((index, input[i]))
                break
        else:
            tree[parent] = [(index, input[i])]
            
        output.append((parent, input[i]))
        index += 1
        i += 1 
    return output

def LZ78_decode(code):
    result = ''
    for parent, token in code:
        result += outputToEntry(code, (parent, token))
    return result


s = "ABRACADABRARABARABARA"
# code = LZ77_encode('', s)
# print(LZ77_decode(code))
# code = LZ78_encode(s)
# print(LZ78_decode(code))
file = 'Bonuri.xlsx'
fileOut = open('COMPRESSED_EXCEL_32KB.txt', 'w')
output = LZ77_encode(file)
print("Done compressing!")
fileOut.write(";".join([str(i) for i in output]))
fileOut.close()