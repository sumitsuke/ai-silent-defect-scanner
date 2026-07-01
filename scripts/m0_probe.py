"""M0 probe: (1) local generation determinism (same seed/opts/threads -> 2x -> hash),
(2) per-step timing (generate / ruff / semgrep). No fabrication: prints raw measured values."""
import time, hashlib, json, subprocess, sys, os, urllib.request

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:1.5b"
OPTS = {"seed": 0, "temperature": 0, "num_ctx": 2048, "num_thread": 4,
        "top_k": 1, "top_p": 1, "num_predict": 256}
PROMPT = ("Write a single Python function `load_config(path)` that reads a JSON file "
          "at `path` and returns the parsed dict. Return only code, no explanation.")

def gen():
    body = json.dumps({"model": MODEL, "prompt": PROMPT, "stream": False,
                       "options": OPTS}).encode()
    req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
    t = time.perf_counter()
    with urllib.request.urlopen(req, timeout=600) as r:
        out = json.loads(r.read())
    dt = time.perf_counter() - t
    return out.get("response", ""), dt

def sha(s): return hashlib.sha256(s.encode("utf-8", "replace")).hexdigest()[:16]

print("== generation determinism (same seed/opts/threads, 2 runs) ==")
t1, d1 = gen()
t2, d2 = gen()
print(f"run1: {len(t1)} chars, sha={sha(t1)}, {d1:.1f}s (incl cold start)")
print(f"run2: {len(t2)} chars, sha={sha(t2)}, {d2:.1f}s")
print(f"IDENTICAL: {sha(t1)==sha(t2)}  (byte-equal: {t1==t2})")

# save one sample for pipeline timing
os.makedirs("results", exist_ok=True)
p = "results/_m0_sample.py"
open(p, "w", encoding="utf-8").write(t1)

print("\n== per-step timing on generated sample ==")
def timed(cmd):
    t = time.perf_counter()
    r = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    return time.perf_counter() - t, r.returncode

ruff = os.path.expanduser(r"~/AppData/Local/Programs/Python/Python312/Scripts/ruff.exe")
if not os.path.exists(ruff): ruff = "ruff"
dt, rc = timed([ruff, "check", "--select", "S110,S112,BLE001,E722", p])
print(f"ruff check: {dt:.2f}s (rc={rc})")

semgrep = os.path.join(".venv", "Scripts", "semgrep.exe")
rule = "results/_m0_rule.yml"
open(rule, "w", encoding="utf-8").write(
"""rules:
  - id: silent-none
    message: swallow
    languages: [python]
    severity: ERROR
    patterns:
      - pattern: |
          try:
            ...
          except $E:
            return None
""")
dt, rc = timed([semgrep, "scan", "--config", rule, p, "--quiet"])
print(f"semgrep scan: {dt:.2f}s (rc={rc})")

print("\n== generated sample (first 500 chars) ==")
print(t1[:500])
