"""Read-only reclassification of the frozen 7B footnote corpus (raw7b/).
Does NOT call Ollama and does NOT regenerate — safe to run repeatedly.
Writes results/footnote_7b.csv. (To REGENERATE raw7b/ from the model, use
scripts/footnote_7b.py, which is destructive — see README.)
Run: PYTHONUTF8=1 python scripts/reclassify_7b.py"""
import ast, glob, os, re, csv, collections
LOGY = re.compile(r"\b(log|logger|logging|print|warn|warning|error|critical|exception)\b", re.I)
DC = {"None", "[]", "{}", "0", "False", "0.0", '""', "''"}

def unp(n):
    try: return ast.unparse(n).strip()
    except Exception: return "?"

def cpy(s):
    try: t = ast.parse(s)
    except Exception: return "parse_error", "", False
    fn = t.body[0] if t.body and isinstance(t.body[0], (ast.FunctionDef, ast.AsyncFunctionDef)) else None
    doc = bool(ast.get_docstring(fn)) if fn else False
    tries = [n for n in ast.walk(t) if isinstance(n, ast.Try)]
    if not tries: return "no_try_except", "", doc
    v, note = "proper", ""
    for x in tries:
        for h in x.handlers:
            hl = LOGY.search("\n".join(unp(z) for z in h.body))
            hr = any(isinstance(n, ast.Raise) for n in ast.walk(h))
            op = len(h.body) == 1 and isinstance(h.body[0], ast.Pass)
            rd = any(isinstance(n, ast.Return) and n.value is not None and unp(n.value) in DC for n in h.body)
            if op: v, note = "swallow_cand", "except:pass"
            elif rd and not hr and not hl: v, note = "swallow_cand", "return-default,no-log/raise"
    return v, note, doc

CATCH = re.compile(r"catch\s*(\([^)]*\))?\s*\{([^{}]*)\}", re.S)
def cts(s):
    if "catch" not in s: return "no_try_except", "", False
    v, note = "proper", ""
    for m in CATCH.finditer(s):
        b = m.group(2).strip()
        if b == "": v, note = "swallow_cand", "empty-catch"
        elif re.search(r"return\s+(null|undefined|\[\]|\{\}|false|''|\"\")\s*;?", b) and "throw" not in b and not LOGY.search(b):
            v, note = "swallow_cand", "return-default"
    return v, note, False

rows = []
for f in sorted(glob.glob("raw7b/**/*.*", recursive=True)):
    f = f.replace("\\", "/"); base = os.path.basename(f)
    lang = "python" if f.endswith(".py") else "typescript"
    v, note, doc = (cpy if lang == "python" else cts)(open(f, encoding="utf-8").read())
    rows.append(dict(file=base, task=base.rsplit("_s", 1)[0], language=lang,
                     classification=v, note=note, py_has_docstring=doc))
os.makedirs("results", exist_ok=True)
with open("results/footnote_7b.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["file", "task", "language", "classification", "note", "py_has_docstring"])
    w.writeheader(); w.writerows(rows)
for lang in ("python", "typescript"):
    c = collections.Counter(r["classification"] for r in rows if r["language"] == lang)
    print(f"[{lang}] {dict(c)}")
print("swallow_cand:", [(r["file"], r["note"], r["py_has_docstring"]) for r in rows if r["classification"] == "swallow_cand"])
print(f"wrote results/footnote_7b.csv ({len(rows)} rows)")
