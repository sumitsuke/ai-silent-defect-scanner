"""Generate N samples per task via Ollama (temp>0 for variation; seed fixed per sample
so each sample is reproducible). Saves extracted code to raw/{lang}/{id}_s{seed}.{ext}."""
import json, os, re, sys, time, urllib.request

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
MODEL = "qwen2.5-coder:1.5b"
OLLAMA = "http://localhost:11434/api/generate"
# temp>0 → varied samples; all other opts fixed; seed varied per sample (reproducible)
BASEOPTS = {"temperature": 0.7, "num_ctx": 2048, "num_predict": 384,
            "num_thread": 4, "top_k": 40, "top_p": 0.9}

def extract_code(text):
    m = re.search(r"```[a-zA-Z0-9]*\s*\n(.*?)```", text, re.S)
    return (m.group(1) if m else text).strip() + "\n"

def gen(prompt, seed):
    opts = dict(BASEOPTS, seed=seed)
    body = json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "options": opts}).encode()
    req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read()).get("response", "")

tasks = json.load(open("tasks/tasks.json", encoding="utf-8"))
total = len(tasks) * N
done = 0; t0 = time.perf_counter()
for tk in tasks:
    d = os.path.join("raw", tk["language"]); os.makedirs(d, exist_ok=True)
    for seed in range(N):
        try:
            code = extract_code(gen(tk["prompt"], seed))
        except Exception as e:
            code = f"# GEN_ERROR seed={seed}: {e}\n"
        open(os.path.join(d, f'{tk["id"]}_s{seed}.{tk["ext"]}'), "w", encoding="utf-8").write(code)
        done += 1
    el = time.perf_counter() - t0
    print(f"[{done}/{total}] {tk['id']} done  ({el:.0f}s elapsed)", flush=True)
print(f"GENERATION COMPLETE: {done} samples in {time.perf_counter()-t0:.0f}s")
