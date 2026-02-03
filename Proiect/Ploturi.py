import ast
from pathlib import Path
import time
import matplotlib.pyplot as plt
from functii_utile import findMatch, outputToEntry, to_matrix


def LZ77_encode(file, _windowLength = 2**14, _searchBufferProcent = 0.875, _min_match=2, writeOut = False):
    windowLength = _windowLength
    search_buffer = int(_searchBufferProcent * windowLength)
    look_ahead_buffer = windowLength - search_buffer
    
    output = []
    numLiterals = 0
    numRefs = 0
    sumMatchLen = 0
    
    t0 = time.time()
    
    with open(file, 'r', encoding = 'utf-8', errors = 'replace') as f:
        window = ''
        input = f.read(look_ahead_buffer)
        while input:
            d, l, c = findMatch(window, input, _min_match)
            output.append((d,l,c))
            
            if d == 0 and l == 0:
                numLiterals += 1
            else:
                numRefs += 1
                sumMatchLen += l
            
            consume = l + 1 if c is not None else l
            window += input[:consume]
            if len(window) > search_buffer:
                window = window[-search_buffer:]
            input = input[consume:] + f.read(consume)

    encMs = (time.time() - t0) * 1e3
    
    serialized = ";".join(str(tup) for tup in output)
    compressed_bytes = len(serialized.encode("utf-8"))

    if writeOut:
        fisierComprimat = 'COMPRESSED_2MB_4KB.txt' 
        with open(fisierComprimat, 'w', encoding = 'utf-8') as out:
            out.write(";".join([str(tup) for tup in output]))
        
    avgMatchLen = (sumMatchLen / numRefs) if numRefs > 0 else 0.0
    originalBytes = Path(file).stat().st_size
    ratio = compressed_bytes / originalBytes if originalBytes else 0.0

    return {
        "compressed_bytes": compressed_bytes,
        "ratio": ratio,
        "enc_ms": encMs,
        "num_tokens": len(output),
        "num_literals": numLiterals,
        "num_refs": numRefs,
        "avg_match_len": avgMatchLen
    }

def LZ77_decode(file):
    f = open(file)
    code = f.read() \
            .replace('(', '') \
            .replace(')', '') \
            .split(';') 
    f.close()
    code = [(int(tuple[0]),
             int(tuple[1]),
             ast.literal_eval(tuple[2])) for tup in code if (tuple := tup.split(', '))]
    result = ''
    for (d,l,c) in code:
        if d != 0:
            result += result[len(result)-d : len(result)-d+l]
        result += c if c is not None else ''
    return result

def LZ78_encode(file):
    input = ''
    with open(file) as f:
        input = f.read() + '$'

    tree = {}
    index = 1
    output = [(None, '')]
    i = 0
    while i < len(input):
        parent = 0
        while tree.get(parent) and i < len(input):
            matched = False
            for child, token in tree[parent]:
                if i >= len(input):
                    break
                if token == input[i]:
                    parent = child
                    i += 1
                    matched = True
                    break
                
            if not matched:
                if i >= len(input):
                    break
                tree[parent].append((index, input[i]))
                break
        else:
            if i < len(input):
                tree[parent] = [(index, input[i])]
                
        if i >= len(input):
            break
            
        output.append((parent, input[i]))
        index += 1
        i += 1 
    return output

def LZ78_decode(code):
    result = ''
    for parent, token in code:
        result += outputToEntry(code, (parent, token))
    return result

def LZ77_analysis(file):
    windowLengths = [2**14, 2**15, 2**16, 2**17]
    searchBufferProcents = [7/8, 15/16, 31/32]
    minMatches = [2, 3, 4, 5]

    resultsSize = {}
    resultsTime = {}
    resultsRatio = {}
    resultsTokens = {}
    resultsAvgLen = {}

    for m in minMatches:
        resultsSize[m] = {}
        resultsTime[m] = {}
        resultsRatio[m] = {}
        resultsTokens[m] = {}
        resultsAvgLen[m] = {}
        
        for W in windowLengths:
            resultsSize[m][W] = []
            resultsTime[m][W] = []
            resultsRatio[m][W] = []
            resultsTokens[m][W] = []
            resultsAvgLen[m][W] = []
            
            for p in searchBufferProcents:
                res = LZ77_encode(file, W, p, m)

                resultsSize[m][W].append(res["compressed_bytes"])
                resultsTime[m][W].append(res["enc_ms"])
                resultsRatio[m][W].append(res["ratio"])
                resultsTokens[m][W].append(res["num_tokens"])
                resultsAvgLen[m][W].append(res["avg_match_len"])

    # =========================
    # 1) Heatmaps: ratio + time (câte un set per min_match)
    # =========================

    for m in minMatches:
        ratioZ = to_matrix(resultsRatio[m], windowLengths, searchBufferProcents)
        timeZ  = to_matrix(resultsTime[m],  windowLengths, searchBufferProcents)

        # --- Heatmap RATIO ---
        plt.figure(figsize=(7, 4.5))
        plt.imshow(ratioZ, aspect="auto", origin="lower")
        plt.colorbar(label="compression ratio (compressed/original)")

        plt.xticks(
            range(len(searchBufferProcents)),
            [f"{p:.3f}" for p in searchBufferProcents],
            rotation=0
        )
        plt.yticks(range(len(windowLengths)), windowLengths)

        plt.xlabel("searchBufferProcent")
        plt.ylabel("windowLength")
        plt.title(f"Compression ratio heatmap (min_match={m})")
        plt.tight_layout()
        plt.savefig(f"Results/Compression ratio heatmap (min_match={m}).svg", format="svg")
        
        # --- Heatmap TIME ---
        plt.figure(figsize=(7, 4.5))
        plt.imshow(timeZ, aspect="auto", origin="lower")
        plt.colorbar(label="encode time (ms)")

        plt.xticks(
            range(len(searchBufferProcents)),
            [f"{p:.3f}" for p in searchBufferProcents],
            rotation=0
        )
        plt.yticks(range(len(windowLengths)), windowLengths)

        plt.xlabel("searchBufferProcent")
        plt.ylabel("windowLength")
        plt.title(f"Encode time heatmap (min_match={m})")
        plt.tight_layout()
        plt.savefig(f"Results/Encode time heatmap (min_match={m}).svg", format="svg")


    # =========================
    # 2) Line plots: ratio vs windowLength (o linie per procent), câte un plot per min_match
    # =========================

    for m in minMatches:
        plt.figure(figsize=(7, 4.5))

        for j, p in enumerate(searchBufferProcents):
            ys = [resultsRatio[m][W][j] for W in windowLengths]
            plt.plot(windowLengths, ys, marker="o", label=f"p={p:.3f}")

        plt.xscale("log", base=2)
        plt.xlabel("windowLength")
        plt.ylabel("compression ratio")
        plt.title(f"Ratio vs windowLength (min_match={m})")
        plt.grid(True, linewidth=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"Results/Ratio vs windowLength (min_match={m}).svg", format="svg")


    # =========================
    # 3) Pareto scatter: time vs ratio
    #    + variantă colorată pe min_match 
    # =========================

    plt.figure(figsize=(7, 4.5))

    for m in minMatches:
        xs, ys = [], []
        for W in windowLengths:
            for j, p in enumerate(searchBufferProcents):
                xs.append(resultsTime[m][W][j])
                ys.append(resultsRatio[m][W][j])
        plt.scatter(xs, ys, label=f"min_match={m}")

    plt.xlabel("encode time (ms)")
    plt.ylabel("compression ratio")
    plt.title("Pareto scatter: time vs compression (colored by min_match)")
    plt.grid(True, linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("Results/Pareto scatter: time vs compression (colored by min_match).svg", format="svg")


    # =========================
    # 4) Pareto scatter cu puncte cheie marcate:
    #    best compression, best speed, balanced
    # =========================

    points = []
    for m in minMatches:
        for W in windowLengths:
            for j, p in enumerate(searchBufferProcents):
                t = resultsTime[m][W][j]
                r = resultsRatio[m][W][j]
                points.append((t, r, m, W, p))

    # best compression = ratio minim
    best_c = min(points, key=lambda x: x[1])
    # best speed = time minim
    best_s = min(points, key=lambda x: x[0])

    t_vals = [x[0] for x in points]
    r_vals = [x[1] for x in points]
    t_min, t_max = min(t_vals), max(t_vals)
    r_min, r_max = min(r_vals), max(r_vals)

    def score(pt, w_r=0.6, w_t=0.4):
        t, r = pt[0], pt[1]
        t_norm = (t - t_min) / (t_max - t_min + 1e-12)
        r_norm = (r - r_min) / (r_max - r_min + 1e-12)
        return w_r * r_norm + w_t * t_norm

    best_bal = min(points, key=score)

    # plot
    plt.figure(figsize=(7, 4.5))

    for m in minMatches:
        xs, ys = [], []
        for (t, r, mm, W, p) in points:
            if mm == m:
                xs.append(t)
                ys.append(r)
        plt.scatter(xs, ys, label=f"min_match={m}")

    plt.scatter([best_c[0]], [best_c[1]], marker="X", s=200,
                label=f"best compression (m={best_c[2]}, W={best_c[3]}, p={best_c[4]:.3f})")
    plt.scatter([best_s[0]], [best_s[1]], marker="X", s=200,
                label=f"best speed (m={best_s[2]}, W={best_s[3]}, p={best_s[4]:.3f})")
    plt.scatter([best_bal[0]], [best_bal[1]], marker="X", s=200,
                label=f"balanced (m={best_bal[2]}, W={best_bal[3]}, p={best_bal[4]:.3f})")

    plt.xlabel("encode time (ms)")
    plt.ylabel("compression ratio")
    plt.title("Pareto scatter (key points marked)")
    plt.grid(True, linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("Results/Pareto scatter (key points marked).svg", format="svg")


    # =========================
    # 5) heatmap pentru avg_match_len (câte una per min_match)
    # =========================

    for m in minMatches:
        avgLenZ = to_matrix(resultsAvgLen[m], windowLengths, searchBufferProcents)

        plt.figure(figsize=(7, 4.5))
        plt.imshow(avgLenZ, aspect="auto", origin="lower")
        plt.colorbar(label="avg match length (only references)")

        plt.xticks(
            range(len(searchBufferProcents)),
            [f"{p:.3f}" for p in searchBufferProcents],
            rotation=0
        )
        plt.yticks(range(len(windowLengths)), windowLengths)

        plt.xlabel("searchBufferProcent")
        plt.ylabel("windowLength")
        plt.title(f"Average match length heatmap (min_match={m})")
        plt.tight_layout()
        plt.savefig(f"Results/Average match length heatmap (min_match={m}).svg", format="svg")

def median(xs):
    xs = sorted(xs)
    return xs[len(xs)//2]

def lz78_metrics_wrapper(file):
    originalBytes = Path(file).stat().st_size

    t0 = time.perf_counter()
    output = LZ78_encode(file)
    encMs = (time.perf_counter() - t0) * 1e3

    serialized = ";".join(str(tup) for tup in output)
    compressed_bytes = len(serialized.encode("utf-8"))
    ratio = compressed_bytes / originalBytes if originalBytes else 0.0

    return {
        "enc_ms": encMs,
        "compressed_bytes": compressed_bytes,
        "ratio": ratio,
        "num_tokens": len(output)
    }


def compare_on_existing_files(files, repeats=3, out_dir="Results"):
    Path(out_dir).mkdir(exist_ok=True)

    files = [Path(f) for f in files]
    for f in files:
        if not f.exists():
            raise FileNotFoundError(f"Nu gasesc fisierul: {f}")

    labels = [f.stem for f in files]

    lz77_time, lz77_ratio = [], []
    lz78_time, lz78_ratio = [], []

    for f in files:
        t_list, r_list = [], []
        for _ in range(repeats):
            res = LZ77_encode(str(f))
            t_list.append(res["enc_ms"])
            r_list.append(res["ratio"])
        lz77_time.append(median(t_list))
        lz77_ratio.append(median(r_list))

        t_list, r_list = [], []
        for _ in range(repeats):
            res = lz78_metrics_wrapper(str(f))
            t_list.append(res["enc_ms"])
            r_list.append(res["ratio"])
        lz78_time.append(median(t_list))
        lz78_ratio.append(median(r_list))

        print(f"{f.name:28s} | "
              f"LZ77: {lz77_time[-1]:8.2f} ms, ratio={lz77_ratio[-1]:.4f} | "
              f"LZ78: {lz78_time[-1]:8.2f} ms, ratio={lz78_ratio[-1]:.4f}")

    # -------------------------
    # GRAFIC 1: Compression ratio
    # -------------------------
    x = list(range(len(labels)))
    width = 0.35

    plt.figure(figsize=(10, 4.8))
    plt.bar([i - width/2 for i in x], lz77_ratio, width=width,
            label="LZ77 (m=2, W=2^14, p=0.875)")
    plt.bar([i + width/2 for i in x], lz78_ratio, width=width, label="LZ78")

    plt.xticks(x, labels, rotation=15, ha="right")
    plt.ylabel("compression ratio (compressed/original)  ↓ mai mic = mai bine")
    plt.title("Comparatie compresie: LZ77 vs LZ78 (fisiere existente)")
    plt.grid(True, axis="y", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(Path(out_dir) / "compare_ratio_LZ77_vs_LZ78.svg", format="svg")

    # -------------------------
    # GRAFIC 2: Encode time
    # -------------------------
    plt.figure(figsize=(10, 4.8))
    plt.bar([i - width/2 for i in x], lz77_time, width=width, label="LZ77")
    plt.bar([i + width/2 for i in x], lz78_time, width=width, label="LZ78")

    plt.xticks(x, labels, rotation=15, ha="right")
    plt.ylabel("encode time (ms)  ↓ mai mic = mai bine")
    plt.title("Comparatie timp de codare: LZ77 vs LZ78 (fisiere existente)")
    plt.grid(True, axis="y", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(Path(out_dir) / "compare_time_LZ77_vs_LZ78.svg", format="svg")

    plt.show()


if __name__ == '__main__':
    FILES = [
        "test input/repeat.txt",
        "test input/text natural.txt",
        "test input/log.txt",
        "test input/random.txt"
    ]
    compare_on_existing_files(FILES, repeats=3, out_dir="Results")