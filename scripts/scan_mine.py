"""Try the scanner on YOUR repo: scan a directory, print the failure-handling
distribution (no_try_except / proper / swallow_cand) and list swallow CANDIDATES.

IMPORTANT: candidates are what a machine can surface. Whether a candidate is a
legitimate fallback or a bug-hiding swallow is an intent judgement (function role,
caller contract, spec) that this tool does NOT make — that last step is human.

Usage:  PYTHONUTF8=1 python scripts/scan_mine.py <DIR>
Requires: pip install semgrep  (optional; classifier works without it)"""
import ast, os, re, sys, glob, subprocess, json, collections

LOGY = re.compile(r"\b(log|logger|logging|print|warn|warning|error|critical|exception)\b", re.I)
DC = {"None", "[]", "{}", "0", "False", "0.0", '""', "''"}
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def unp(n):
    try: return ast.unparse(n).strip()
    except Exception: return "?"

def classify_py(s):
    try: t = ast.parse(s)
    except Exception: return "parse_error"
    tries = [n for n in ast.walk(t) if isinstance(n, ast.Try)]
    if not tries: return "no_try_except"
    v = "proper"
    for x in tries:
        for h in x.handlers:
            hl = LOGY.search("\n".join(unp(z) for z in h.body))
            hr = any(isinstance(n, ast.Raise) for n in ast.walk(h))
            op = len(h.body) == 1 and isinstance(h.body[0], ast.Pass)
            rd = any(isinstance(n, ast.Return) and n.value is not None and unp(n.value) in DC for n in h.body)
            if op or (rd and not hr and not hl): v = "swallow_cand"
    return v

CATCH = re.compile(r"catch\s*(\([^)]*\))?\s*\{([^{}]*)\}", re.S)
def classify_ts(s):
    if "catch" not in s: return "no_try_except"
    v = "proper"
    for m in CATCH.finditer(s):
        b = m.group(2).strip()
        if b == "" or (re.search(r"return\s+(null|undefined|\[\]|\{\}|false|''|\"\")\s*;?", b) and "throw" not in b and not LOGY.search(b)):
            v = "swallow_cand"
    return v

def main(d):
    files = [f for ext in ("py", "ts", "js", "tsx", "jsx")
             for f in glob.glob(os.path.join(d, "**", f"*.{ext}"), recursive=True)]
    files = [f for f in files if "node_modules" not in f and ".venv" not in f]
    if not files:
        print(f"no .py/.ts/.js files under {d}"); return
    dist = collections.Counter(); cands = []
    for f in files:
        try: s = open(f, encoding="utf-8", errors="replace").read()
        except Exception: continue
        lang = "python" if f.endswith(".py") else "typescript"
        v = (classify_py if lang == "python" else classify_ts)(s)
        dist[v] += 1
        if v == "swallow_cand": cands.append(f)
    print(f"== failure-handling distribution over {sum(dist.values())} files in {d} ==")
    for k in ("no_try_except", "proper", "swallow_cand", "parse_error"):
        if dist.get(k): print(f"  {k:16} {dist[k]}")
    # Semgrep candidates (optional)
    sem = None
    for cand in (os.path.join(HERE, ".venv", "Scripts", "semgrep.exe"),
                 os.path.join(HERE, ".venv", "bin", "semgrep"), "semgrep"):
        if os.path.exists(cand) or cand == "semgrep":
            sem = cand; break
    print("\n== swallow CANDIDATES (machine-surfaced; human must adjudicate legit-vs-swallow) ==")
    printed = False
    try:
        cfgs = [os.path.join(HERE, "rules", "silent-fallbacks-python.yml"),
                os.path.join(HERE, "rules", "silent-fallbacks-typescript.yml")]
        cmd = [sem, "scan"] + sum([["--config", c] for c in cfgs], []) + [d, "--json", "--quiet"]
        env = dict(os.environ, PYTHONUTF8="1")
        res = subprocess.run(cmd, capture_output=True, text=True, env=env)
        for r in json.loads(res.stdout).get("results", []):
            print(f"  {r['path']}:{r['start']['line']}  [{r['check_id'].split('.')[-1]}]"); printed = True
    except Exception as e:
        print(f"  (semgrep step skipped: {e})")
    for f in cands:
        print(f"  {f}  [classifier: swallow_cand]"); printed = True
    if not printed:
        print("  (none surfaced)")
    print("\nNote: a candidate is not a verdict. Open each and read the function's role,"
          "\ncaller contract, and spec/docstring before deciding legit fallback vs silent swallow.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: PYTHONUTF8=1 python scripts/scan_mine.py <DIR>"); sys.exit(2)
    main(sys.argv[1])
