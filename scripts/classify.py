"""3-way classify each generation: unhandled / proper / swallow-candidate.
Python via ast (robust); TS via regex heuristics. Prints distribution +
lists swallow-candidates for manual review. Measured, not fabricated."""
import ast, glob, os, re, collections

LOGY = re.compile(r"\b(log|logger|logging|print|warn|warning|error|critical|exception)\b", re.I)
DEFAULT_CONSTS = {"None", "[]", "{}", "0", "False", "0.0", '""', "''"}

def const_str(node):
    try: return ast.unparse(node).strip()
    except Exception: return "?"

def classify_py(src):
    try: tree = ast.parse(src)
    except Exception: return "parse_error", ""
    tries = [n for n in ast.walk(tree) if isinstance(n, ast.Try)]
    if not tries: return "unhandled", ""
    verdict = "proper"; note = ""
    for t in tries:
        for h in t.handlers:
            body = h.body
            has_raise = any(isinstance(n, ast.Raise) for n in ast.walk(h))
            # evaluate log-keywords on the HANDLER BODY only — including the header
            # (e.g. `except Exception:`) would false-match "exception"/"error" and
            # wrongly promote a silent `except Exception: return None` to proper.
            has_log = LOGY.search("\n".join(ast.unparse(s) for s in body))
            only_pass = len(body) == 1 and isinstance(body[0], ast.Pass)
            ret_default = any(isinstance(n, ast.Return) and n.value is not None and const_str(n.value) in DEFAULT_CONSTS for n in body)
            if only_pass:
                verdict = "swallow_cand"; note = "except:pass"
            elif ret_default and not has_raise and not has_log:
                verdict = "swallow_cand"; note = "return-default,no-log/raise"
    return verdict, note

CATCH = re.compile(r"catch\s*(\([^)]*\))?\s*\{([^{}]*)\}", re.S)
def classify_ts(src):
    if "catch" not in src: return "unhandled", ""
    verdict = "proper"; note = ""
    for m in CATCH.finditer(src):
        body = m.group(2).strip()
        if body == "":
            verdict = "swallow_cand"; note = "empty-catch"
        elif re.search(r"return\s+(null|undefined|\[\]|\{\}|false|''|\"\")\s*;?", body) and "throw" not in body and not LOGY.search(body):
            verdict = "swallow_cand"; note = "return-default,no-log/throw"
    return verdict, note

files = sorted(f.replace("\\","/") for f in glob.glob("raw/**/*.*", recursive=True))
counts = collections.defaultdict(lambda: collections.Counter())
cands = []
for f in files:
    src = open(f, encoding="utf-8").read()
    if src.startswith("# GEN_ERROR"): continue
    lang = "python" if f.endswith(".py") else "typescript"
    v, note = (classify_py if lang=="python" else classify_ts)(src)
    counts[lang][v] += 1
    if v == "swallow_cand": cands.append((f, note))

print("== 3-way classification (per language) ==")
for lang in ("python","typescript"):
    c = counts[lang]; tot = sum(c.values())
    handled = tot - c["unhandled"] - c["parse_error"]
    print(f"[{lang}] total={tot}  unhandled={c['unhandled']}  proper={c['proper']}  swallow_cand={c['swallow_cand']}  parse_error={c['parse_error']}")
    sw = c["swallow_cand"]
    print(f"   handled={handled}  conditional swallow rate = swallow/(proper+swallow) = {sw}/{c['proper']+sw} = {(100*sw/(c['proper']+sw) if (c['proper']+sw) else 0):.0f}%")
print(f"\n== swallow-candidates for manual review ({len(cands)}) ==")
for f, note in cands: print(f"  {f}  [{note}]")
