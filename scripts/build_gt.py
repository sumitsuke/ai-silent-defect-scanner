"""Build results/gt.csv = the human ground-truth / adjudication layer.
Machine fields (handling/subtype/returns_default/has_log/has_raise/intent) are
computed from AST/regex for ALL 120 generations. human_verdict is populated only
for the candidates and boundary cases the author actually opened and adjudicated
(the rest = 'not_adjudicated' = clear proper or clear bare, no default-return).
This is the transparency layer behind the article's 'candidate=machine / adjudication=human'.
Reproduce: PYTHONUTF8=1 python scripts/build_gt.py"""

import ast, glob, os, re, csv

# TypeScript shape columns (added 2026-09-17) need tree-sitter; fail loudly rather than write blanks.
from tree_sitter import Language, Parser
import tree_sitter_typescript as _tst

TS_PARSER = Parser(Language(_tst.language_typescript()))
LOGY = re.compile(r"\b(log|logger|logging|print|warn|warning|error|critical|exception)\b", re.I)
DC = {"None", "[]", "{}", "0", "False", "0.0", '""', "''"}


def unp(n):
    try:
        return ast.unparse(n).strip()
    except Exception:
        return "?"


def analyze_py(s):
    try:
        t = ast.parse(s)
    except Exception:
        return dict(handling="parse_error", subtype="", returns_default="", has_log="", has_raise="", intent="")
    fn = t.body[0] if t.body and isinstance(t.body[0], (ast.FunctionDef, ast.AsyncFunctionDef)) else None
    doc = bool(ast.get_docstring(fn)) if fn else False
    has_raise = any(isinstance(n, ast.Raise) for n in ast.walk(t))
    has_log = bool(LOGY.search(s))
    ret_def = any(isinstance(n, ast.Return) and n.value is not None and unp(n.value) in DC for n in ast.walk(t))
    tries = [n for n in ast.walk(t) if isinstance(n, ast.Try)]
    intent = "docstring" if doc else ""  # comment-level intent is filled per-sample below
    if not tries:
        sub = "raise" if has_raise else ("guard_default" if ret_def else "bare")
        return dict(
            handling="no_try_except",
            subtype=sub,
            returns_default="Y" if ret_def else "N",
            has_log="Y" if has_log else "N",
            has_raise="Y" if has_raise else "N",
            intent=intent,
        )
    handling = "proper"
    handler_def = False
    for x in tries:
        for h in x.handlers:
            hl = LOGY.search("\n".join(unp(z) for z in h.body))
            hr = any(isinstance(n, ast.Raise) for n in ast.walk(h))
            op = len(h.body) == 1 and isinstance(h.body[0], ast.Pass)
            rd = any(isinstance(n, ast.Return) and n.value is not None and unp(n.value) in DC for n in h.body)
            if rd:
                handler_def = True
            if op or (rd and not hr and not hl):
                handling = "swallow_cand"
    # 2026-09-17: handler があっても subtype を空にしない（読者の指摘＝空だと guard 集合を gt.csv から数えられない）。
    #   guard_default   = default return が except handler の外にある（handler の中には無い）
    #   handler_default = default return が handler の中だけ
    #   both            = 両方にある
    #   guard の定義は「except handler の外で default を return する」＝Return ノードのうち、どの handler 本体にも属さないもの
    in_handler = set()
    for x in tries:
        for h in x.handlers:
            for n in ast.walk(h):
                in_handler.add(id(n))
    guard_def = any(
        isinstance(n, ast.Return) and n.value is not None and unp(n.value) in DC and id(n) not in in_handler
        for n in ast.walk(t)
    )
    sub = (
        "both"
        if (guard_def and handler_def)
        else ("guard_default" if guard_def else ("handler_default" if handler_def else ""))
    )
    return dict(
        handling=handling,
        subtype=sub,
        returns_default="Y" if ret_def else "N",
        has_log="Y" if has_log else "N",
        has_raise="Y" if has_raise else "N",
        intent=intent,
    )


CATCH = re.compile(r"catch\s*(\([^)]*\))?\s*\{([^{}]*)\}", re.S)
TS_DEFAULTS = {"null", "undefined", "[]", "{}", "false", "0", "''", '""', "``"}


def _ts_walk(n):
    yield n
    for c in n.children:
        yield from _ts_walk(c)


def _ts_default_return(n, src):
    """return_statement whose value is a default (null/undefined/[]/{}/false/0/''). Bare `return;` is not."""
    exprs = [c for c in n.children if c.type not in ("return", ";")]
    if not exprs:
        return False
    e = exprs[0]
    if src[e.start_byte : e.end_byte].decode("utf-8").strip() in TS_DEFAULTS:
        return True
    if e.type == "array" and not [c for c in e.children if c.type not in ("[", "]")]:
        return True
    if e.type == "object" and not [c for c in e.children if c.type not in ("{", "}")]:
        return True
    return False


def ts_shape(s):
    """2026-09-17: shape columns for TypeScript via tree-sitter (same definitions as the Python side).
    subtype: no catch -> raise / guard_default / bare; with catch -> guard_default / handler_default / both / ''.
    Also returns the AST's own handling verdict so build time can print where it disagrees with the regex."""
    src = s.encode("utf-8")
    root = TS_PARSER.parse(src).root_node
    catches = [n for n in _ts_walk(root) if n.type == "catch_clause"]
    throws = any(n.type == "throw_statement" for n in _ts_walk(root))
    in_catch = {n.id for c in catches for n in _ts_walk(c)}
    rets = [n for n in _ts_walk(root) if n.type == "return_statement" and _ts_default_return(n, src)]
    guard_def = any(n.id not in in_catch for n in rets)
    handler_def = any(n.id in in_catch for n in rets)
    if not catches:
        sub = "raise" if throws else ("guard_default" if rets else "bare")
        return dict(
            subtype=sub,
            returns_default="Y" if rets else "N",
            has_raise="Y" if throws else "N",
            handling_ast="no_try_except",
            parse_error=root.has_error,
        )
    handling = "proper"
    for c in catches:
        body = next((x for x in c.children if x.type == "statement_block"), None)
        stmts = [x for x in body.children if x.type not in ("{", "}", "comment")] if body else []
        btxt = src[body.start_byte : body.end_byte].decode("utf-8") if body else ""
        b_throw = any(n.type == "throw_statement" for n in _ts_walk(body)) if body else False
        b_retdef = (
            any(n.type == "return_statement" and _ts_default_return(n, src) for n in _ts_walk(body)) if body else False
        )
        if not stmts or (b_retdef and not b_throw and not LOGY.search(btxt)):
            handling = "swallow_cand"
    sub = (
        "both"
        if (guard_def and handler_def)
        else ("guard_default" if guard_def else ("handler_default" if handler_def else ""))
    )
    return dict(
        subtype=sub,
        returns_default="Y" if rets else "N",
        has_raise="Y" if throws else "N",
        handling_ast=handling,
        parse_error=root.has_error,
    )


def analyze_ts(s):
    # `handling` stays the regex verdict the article's numbers were computed with; shape columns come from the AST.
    has_log = bool(LOGY.search(s))
    shape = ts_shape(s)
    assert not shape["parse_error"], "tree-sitter reported a parse error"
    if "catch" not in s:
        handling = "no_try_except"
    else:
        handling = "proper"
        for m in CATCH.finditer(s):
            b = m.group(2).strip()
            if b == "" or (
                re.search(r"return\s+(null|undefined|\[\]|\{\}|false|''|\"\")\s*;?", b)
                and "throw" not in b
                and not LOGY.search(b)
            ):
                handling = "swallow_cand"
    return dict(
        handling=handling,
        subtype=shape["subtype"],
        returns_default=shape["returns_default"],
        has_log="Y" if has_log else "N",
        has_raise=shape["has_raise"],
        intent="",
        handling_ast=shape["handling_ast"],
    )


# Human adjudications the author actually made (sample_id -> (verdict, intent_override, note))
HUMAN = {
    "py_parse_int_s3": (
        "legit_fallback",
        "docstring",
        "docstring documents 'None if key missing or not convertible' = intended contract",
    ),
    "py_parse_int_s9": ("legit_fallback", "comment", "comment 'Return None if conversion fails' documents intent"),
    # 2026-09-18: the two open TypeScript guard rows, ruled after a reader's re-derivation (dev.to comment 3f6l4). Same rule as py_parse_int_s3/s9:
    # the documented default is the contract. No catch in either file; the default return is the if-guard's else path.
    "ts_parse_int_s0": (
        "legit_fallback",
        "docstring",
        "docstring 'If the conversion is not possible or the value is not a number, it returns null' = intended contract (ruled 2026-09-18; precedent py_parse_int_s3)",
    ),
    "ts_parse_int_s5": (
        "legit_fallback",
        "docstring",
        "docstring '@returns ... otherwise undefined' documents intent (ruled 2026-09-18; precedent py_parse_int_s9)",
    ),
    "py_fetch_json_s2": (
        "problematic_fallback",
        "comment",
        "if-guard returns None on any non-200 status (comment says so), erasing the 404/500/204 distinction; network errors are not swallowed (requests.get is outside any try and raises; corrected 2026-09-24); outside try/except detector scope",
    ),
    "py_fetch_json_s3": (
        "problematic_fallback",
        "comment+log",
        "logs then returns None on failure; same failure-info-erasing fallback; detector scope-out",
    ),
    "py_fetch_json_s7": (
        "problematic_fallback",
        "comment+log",
        "logs then returns None on failure; detector scope-out",
    ),
    "py_fetch_json_s9": (
        "problematic_fallback",
        "comment+log",
        "logs then returns None on failure; detector scope-out",
    ),
    "ts_load_config_s0": (
        "false_positive",
        "",
        "naive Semgrep flagged the trailing demo-block comment-only catch; the real function logs+rethrows (proper)",
    ),
    "ts_load_config_s2": (
        "false_positive",
        "",
        "naive Semgrep flagged the trailing demo-block comment-only catch; the real function logs+throws new Error (proper)",
    ),
}

rows = []
TS_DISAGREE = []  # (sample_id, regex handling, AST handling) — printed, not written; `handling` keeps the published regex verdict
for f in sorted(glob.glob("raw/**/*.*", recursive=True)):
    f = f.replace("\\", "/")
    base = os.path.basename(f)
    sid = base.rsplit(".", 1)[0]
    tid = base.rsplit("_s", 1)[0]
    seed = base.rsplit("_s", 1)[1].split(".")[0]
    lang = "python" if f.endswith(".py") else "typescript"
    s = open(f, encoding="utf-8").read()
    a = (analyze_py if lang == "python" else analyze_ts)(s)
    if lang == "typescript" and a["handling_ast"] != a["handling"]:
        TS_DISAGREE.append((sid, a["handling"], a["handling_ast"]))
    verdict, note = "not_adjudicated", ""
    if sid in HUMAN:
        verdict, intent_override, note = HUMAN[sid]
        if intent_override:
            a["intent"] = intent_override
    elif a["handling"] == "proper":
        verdict = "proper"
    elif a["handling"] == "no_try_except" and a["subtype"] == "raise":
        verdict = "loud_fail"
    rows.append(
        dict(
            sample_id=sid,
            task_id=tid,
            language=lang,
            seed=seed,
            handling=a["handling"],
            subtype=a["subtype"],
            returns_default=a["returns_default"],
            has_log=a["has_log"],
            has_raise=a["has_raise"],
            intent_disclosed=a["intent"],
            human_verdict=verdict,
            review_note=note,
        )
    )

os.makedirs("results", exist_ok=True)
cols = [
    "sample_id",
    "task_id",
    "language",
    "seed",
    "handling",
    "subtype",
    "returns_default",
    "has_log",
    "has_raise",
    "intent_disclosed",
    "human_verdict",
    "review_note",
]
with open("results/gt.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

from collections import Counter

print(f"wrote results/gt.csv ({len(rows)} rows)")
print("human_verdict distribution:", dict(Counter(r["human_verdict"] for r in rows)))
print(
    "TS rows where the tree-sitter handling differs from the regex handling kept in `handling`:", TS_DISAGREE or "none"
)
print(
    "TS guard set (subtype in guard_default/both):",
    sum(1 for r in rows if r["language"] == "typescript" and r["subtype"] in ("guard_default", "both")),
    "rows; adjudicated problematic:",
    sum(
        1
        for r in rows
        if r["language"] == "typescript"
        and r["subtype"] in ("guard_default", "both")
        and r["human_verdict"] == "problematic_fallback"
    ),
)
print("adjudicated (non-trivial) rows:")
for r in rows:
    if r["human_verdict"] in ("legit_fallback", "problematic_fallback", "false_positive"):
        print(
            f"  {r['sample_id']:22} {r['human_verdict']:20} intent={r['intent_disclosed']:12} {r['review_note'][:60]}"
        )
