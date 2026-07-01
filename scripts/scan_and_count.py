"""M2 spike aggregation: run self-made Semgrep rules over raw/, compute swallow
containment rate = (files with >=1 hit)/(files). Per language & per task. Prints examples.
NOTE: spike-level (false-positive tuning is M3). Numbers are measured, not fabricated."""
import json, os, subprocess, collections, glob

SEM = os.path.join(".venv", "Scripts", "semgrep.exe")
CONFIGS = ["rules/silent-fallbacks-python.yml", "rules/silent-fallbacks-typescript.yml"]

files = [f.replace("\\", "/") for f in glob.glob("raw/**/*.*", recursive=True)]
gen_err = [f for f in files if open(f, encoding="utf-8").read().startswith("# GEN_ERROR")]
valid = [f for f in files if f not in gen_err]

cmd = [SEM, "scan"] + sum([["--config", c] for c in CONFIGS], []) + ["raw", "--json", "--quiet"]
res = subprocess.run(cmd, capture_output=True, text=True)
data = json.loads(res.stdout)
hits_by_file = collections.defaultdict(list)
for r in data.get("results", []):
    hits_by_file[r["path"].replace("\\", "/")].append((r["check_id"].split(".")[-1], r["start"]["line"]))

def rate(fileset):
    n = len(fileset); h = sum(1 for f in fileset if hits_by_file.get(f))
    return h, n, (100.0*h/n if n else 0)

print(f"total files={len(files)}  valid={len(valid)}  gen_errors={len(gen_err)}")
h, n, p = rate(valid)
print(f"\n== overall swallow containment (>=1 hit / valid) ==\n  {h}/{n} = {p:.1f}%")

for lang in ("python", "typescript"):
    fs = [f for f in valid if f"/{lang}/" in f]
    h, n, p = rate(fs)
    print(f"  [{lang}] {h}/{n} = {p:.1f}%")

print("\n== per task ==")
tasks = {t["id"]: t for t in json.load(open("tasks/tasks.json", encoding="utf-8"))}
by_task = collections.defaultdict(list)
for f in valid:
    tid = os.path.basename(f).rsplit("_s", 1)[0]
    by_task[tid].append(f)
for tid in tasks:
    if tid in by_task:
        h, n, p = rate(by_task[tid])
        ctrl = " (control)" if "control" in tid else ""
        print(f"  {tid}{ctrl}: {h}/{n} = {p:.0f}%")

print("\n== example hits (first 6) ==")
shown = 0
for f, hs in hits_by_file.items():
    for rule, line in hs:
        print(f"  {f}:{line}  [{rule}]")
        shown += 1
        if shown >= 6: break
    if shown >= 6: break
