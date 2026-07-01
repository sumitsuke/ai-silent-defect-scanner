"""Build results/gt.csv = the human ground-truth / adjudication layer.
Machine fields (handling/subtype/returns_default/has_log/has_raise/intent) are
computed from AST/regex for ALL 120 generations. human_verdict is populated only
for the candidates and boundary cases the author actually opened and adjudicated
(the rest = 'not_adjudicated' = clear proper or clear bare, no default-return).
This is the transparency layer behind the article's 'candidate=machine / adjudication=human'.
Reproduce: PYTHONUTF8=1 python scripts/build_gt.py"""
import ast, glob, os, re, csv
LOGY = re.compile(r"\b(log|logger|logging|print|warn|warning|error|critical|exception)\b", re.I)
DC = {"None", "[]", "{}", "0", "False", "0.0", '""', "''"}

def unp(n):
    try: return ast.unparse(n).strip()
    except Exception: return "?"

def analyze_py(s):
    try: t = ast.parse(s)
    except Exception: return dict(handling="parse_error", subtype="", returns_default="", has_log="", has_raise="", intent="")
    fn = t.body[0] if t.body and isinstance(t.body[0], (ast.FunctionDef, ast.AsyncFunctionDef)) else None
    doc = bool(ast.get_docstring(fn)) if fn else False
    has_raise = any(isinstance(n, ast.Raise) for n in ast.walk(t))
    has_log = bool(LOGY.search(s))
    ret_def = any(isinstance(n, ast.Return) and n.value is not None and unp(n.value) in DC for n in ast.walk(t))
    tries = [n for n in ast.walk(t) if isinstance(n, ast.Try)]
    intent = "docstring" if doc else ""  # comment-level intent is filled per-sample below
    if not tries:
        sub = "raise" if has_raise else ("guard_default" if ret_def else "bare")
        return dict(handling="no_try_except", subtype=sub, returns_default="Y" if ret_def else "N",
                    has_log="Y" if has_log else "N", has_raise="Y" if has_raise else "N", intent=intent)
    handling = "proper"
    for x in tries:
        for h in x.handlers:
            hl = LOGY.search("\n".join(unp(z) for z in h.body))
            hr = any(isinstance(n, ast.Raise) for n in ast.walk(h))
            op = len(h.body) == 1 and isinstance(h.body[0], ast.Pass)
            rd = any(isinstance(n, ast.Return) and n.value is not None and unp(n.value) in DC for n in h.body)
            if op or (rd and not hr and not hl): handling = "swallow_cand"
    return dict(handling=handling, subtype="", returns_default="Y" if ret_def else "N",
                has_log="Y" if has_log else "N", has_raise="Y" if has_raise else "N", intent=intent)

CATCH = re.compile(r"catch\s*(\([^)]*\))?\s*\{([^{}]*)\}", re.S)
def analyze_ts(s):
    has_log = bool(LOGY.search(s)); has_throw = "throw" in s
    if "catch" not in s:
        return dict(handling="no_try_except", subtype="", returns_default="", has_log="Y" if has_log else "N", has_raise="", intent="")
    handling = "proper"
    for m in CATCH.finditer(s):
        b = m.group(2).strip()
        if b == "" or (re.search(r"return\s+(null|undefined|\[\]|\{\}|false|''|\"\")\s*;?", b) and "throw" not in b and not LOGY.search(b)):
            handling = "swallow_cand"
    return dict(handling=handling, subtype="", returns_default="", has_log="Y" if has_log else "N",
                has_raise="Y" if has_throw else "N", intent="")

# Human adjudications the author actually made (sample_id -> (verdict, intent_override, note))
HUMAN = {
    "py_parse_int_s3": ("legit_fallback", "docstring", "docstring documents 'None if key missing or not convertible' = intended contract"),
    "py_parse_int_s9": ("legit_fallback", "comment", "comment 'Return None if conversion fails' documents intent"),
    "py_fetch_json_s2": ("problematic_fallback", "comment", "if-guard returns None on non-200 (comment says so) but erases 404/500/network/empty distinction; outside try/except detector scope"),
    "py_fetch_json_s3": ("problematic_fallback", "comment+log", "logs then returns None on failure; same failure-info-erasing fallback; detector scope-out"),
    "py_fetch_json_s7": ("problematic_fallback", "comment+log", "logs then returns None on failure; detector scope-out"),
    "py_fetch_json_s9": ("problematic_fallback", "comment+log", "logs then returns None on failure; detector scope-out"),
    "ts_load_config_s0": ("false_positive", "", "naive Semgrep flagged the trailing demo-block comment-only catch; the real function logs+rethrows (proper)"),
    "ts_load_config_s2": ("false_positive", "", "naive Semgrep flagged the trailing demo-block comment-only catch; the real function logs+throws new Error (proper)"),
}

rows = []
for f in sorted(glob.glob("raw/**/*.*", recursive=True)):
    f = f.replace("\\", "/")
    base = os.path.basename(f); sid = base.rsplit(".", 1)[0]
    tid = base.rsplit("_s", 1)[0]; seed = base.rsplit("_s", 1)[1].split(".")[0]
    lang = "python" if f.endswith(".py") else "typescript"
    s = open(f, encoding="utf-8").read()
    a = (analyze_py if lang == "python" else analyze_ts)(s)
    verdict, note = "not_adjudicated", ""
    if sid in HUMAN:
        verdict, intent_override, note = HUMAN[sid]
        if intent_override: a["intent"] = intent_override
    elif a["handling"] == "proper":
        verdict = "proper"
    elif a["handling"] == "no_try_except" and a["subtype"] == "raise":
        verdict = "loud_fail"
    rows.append(dict(sample_id=sid, task_id=tid, language=lang, seed=seed,
                     handling=a["handling"], subtype=a["subtype"],
                     returns_default=a["returns_default"], has_log=a["has_log"],
                     has_raise=a["has_raise"], intent_disclosed=a["intent"],
                     human_verdict=verdict, review_note=note))

os.makedirs("results", exist_ok=True)
cols = ["sample_id", "task_id", "language", "seed", "handling", "subtype",
        "returns_default", "has_log", "has_raise", "intent_disclosed", "human_verdict", "review_note"]
with open("results/gt.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)

from collections import Counter
print(f"wrote results/gt.csv ({len(rows)} rows)")
print("human_verdict distribution:", dict(Counter(r["human_verdict"] for r in rows)))
print("adjudicated (non-trivial) rows:")
for r in rows:
    if r["human_verdict"] in ("legit_fallback", "problematic_fallback", "false_positive"):
        print(f"  {r['sample_id']:22} {r['human_verdict']:20} intent={r['intent_disclosed']:12} {r['review_note'][:60]}")
