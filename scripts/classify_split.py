"""Split 3-way classification by failure-prone vs control (1.5B corpus).
Precise numbers for the article (controls are pure-compute => naturally unhandled)."""
import ast, glob, re, collections
LOGY = re.compile(r"\b(log|logger|logging|print|warn|warning|error|critical|exception)\b", re.I)
DC = {"None", "[]", "{}", "0", "False", "0.0", '""', "''"}

def cs(n):
    try: return ast.unparse(n).strip()
    except Exception: return "?"

def cpy(s):
    try: t = ast.parse(s)
    except Exception: return "parse_error"
    tr = [n for n in ast.walk(t) if isinstance(n, ast.Try)]
    if not tr: return "unhandled"
    v = "proper"
    for x in tr:
        for h in x.handlers:
            hr = any(isinstance(n, ast.Raise) for n in ast.walk(h))
            hl = LOGY.search("\n".join(ast.unparse(s) for s in h.body))
            op = len(h.body) == 1 and isinstance(h.body[0], ast.Pass)
            rd = any(isinstance(n, ast.Return) and n.value is not None and cs(n.value) in DC for n in h.body)
            if op: v = "swallow_cand"
            elif rd and not hr and not hl: v = "swallow_cand"
    return v

CATCH = re.compile(r"catch\s*(\([^)]*\))?\s*\{([^{}]*)\}", re.S)
def cts(s):
    if "catch" not in s: return "unhandled"
    v = "proper"
    for m in CATCH.finditer(s):
        b = m.group(2).strip()
        if b == "": v = "swallow_cand"
        elif re.search(r"return\s+(null|undefined|\[\]|\{\}|false|''|\"\")\s*;?", b) and "throw" not in b and not LOGY.search(b): v = "swallow_cand"
    return v

for scope, pred in [("ALL", lambda f: True), ("FAILURE-PRONE", lambda f: "control" not in f), ("CONTROL", lambda f: "control" in f)]:
    cnt = collections.defaultdict(lambda: collections.Counter())
    for f in sorted(glob.glob("raw/**/*.*", recursive=True)):
        f = f.replace("\\", "/")
        if not pred(f): continue
        s = open(f, encoding="utf-8").read()
        if s.startswith("# GEN_ERROR"): continue
        lang = "python" if f.endswith(".py") else "typescript"
        cnt[lang][(cpy if lang == "python" else cts)(s)] += 1
    print(f"== {scope} ==")
    for lang in ("python", "typescript"):
        c = cnt[lang]; tot = sum(c.values()); h = tot - c["unhandled"] - c["parse_error"]; sw = c["swallow_cand"]
        rate = f"{100*sw/h:.0f}%" if h else "n/a"
        print(f"  [{lang}] n={tot} no_try_except={c['unhandled']} proper={c['proper']} swallow_cand={sw}  cond_swallow={sw}/{h}={rate}")
