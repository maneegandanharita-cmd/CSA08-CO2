import time, io

def build_plus(parts):
    text = ""
    for p in parts:
        text += p + ";"
    return text

def build_join(parts):
    return ";".join(parts) + ";"

def build_fstring(parts):
    return "".join(f"{p};" for p in parts)

def build_stringio(parts):
    buf = io.StringIO()
    for p in parts:
        buf.write(p)
        buf.write(";")
    return buf.getvalue()

print(f"{'lines':>8} | {'+= (s)':>9} | {'join (s)':>9} | {'f-string (s)':>12} | {'StringIO (s)':>12} | same")
for n in (1_000, 10_000, 200_000):
    items = [f"Item{i}:Rs{i % 50}" for i in range(n)]
    row = []
    outs = []
    for f in (build_plus, build_join, build_fstring, build_stringio):
        s = time.perf_counter(); out = f(items); row.append(time.perf_counter() - s); outs.append(out)
    print(f"{n:>8} | {row[0]:>9.5f} | {row[1]:>9.5f} | {row[2]:>12.5f} | {row[3]:>12.5f} | {len(set(outs)) == 1}")
