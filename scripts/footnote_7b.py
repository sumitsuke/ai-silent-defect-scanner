"""7B robustness footnote: generate N samples per FAILURE-PRONE task with
qwen2.5-coder:7b, then 3-way classify (unhandled/proper/swallow_cand).
Compares against 1.5B to check if 'unhandled dominates / swallow rare' holds.
Measured, not fabricated. Run with PYTHONUTF8=1."""
import ast, json, os, re, sys, time, urllib.request, collections

N = int(sys.argv[1]) if len(sys.argv) > 1 else 3
MODEL = "qwen2.5-coder:7b"
OLLAMA = "http://localhost:11434/api/generate"
BASEOPTS = {"temperature": 0.7, "num_ctx": 2048, "num_predict": 384,
            "num_thread": 4, "top_k": 40, "top_p": 0.9}
OUT = "raw7b"

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

def extract_code(text):
    m = re.search(r"```[a-zA-Z0-9]*\s*\n(.*?)```", text, re.S)
    return (m.group(1) if m else text).strip() + "\n"

def gen(prompt, seed):
    opts = dict(BASEOPTS, seed=seed)
    body = json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "options": opts}).encode()
    req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1200) as r:
        return json.loads(r.read()).get("response", "")

tasks = [t for t in json.load(open("tasks/tasks.json", encoding="utf-8")) if "control" not in t["id"]]
counts = collections.defaultdict(lambda: collections.Counter())
cands = []
t0 = time.perf_counter(); done = 0; total = len(tasks) * N
for tk in tasks:
    d = os.path.join(OUT, tk["language"]); os.makedirs(d, exist_ok=True)
    for seed in range(N):
        try:
            code = extract_code(gen(tk["prompt"], seed))
        except Exception as e:
            code = f"# GEN_ERROR seed={seed}: {e}\n"
        open(os.path.join(d, f'{tk["id"]}_s{seed}.{tk["ext"]}'), "w", encoding="utf-8").write(code)
        done += 1
        if not code.startswith("# GEN_ERROR"):
            v, note = (classify_py if tk["language"]=="python" else classify_ts)(code)
            counts[tk["language"]][v] += 1
            if v == "swallow_cand": cands.append((f'{tk["id"]}_s{seed}', note))
    print(f"[{done}/{total}] {tk['id']} ({time.perf_counter()-t0:.0f}s)", flush=True)

print(f"\n=== 7B footnote: 3-way classification (N={N}/task, failure-prone only) ===")
for lang in ("python", "typescript"):
    c = counts[lang]; tot = sum(c.values()); sw = c["swallow_cand"]
    handled = tot - c["unhandled"] - c["parse_error"]
    print(f"[{lang}] total={tot} unhandled={c['unhandled']} proper={c['proper']} swallow_cand={sw} parse_error={c['parse_error']}")
    print(f"   conditional swallow = {sw}/{handled} = {(100*sw/handled if handled else 0):.0f}%")
print("\nswallow-candidates:", cands if cands else "(none)")
print(f"TOTAL {time.perf_counter()-t0:.0f}s")
