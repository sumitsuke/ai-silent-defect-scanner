# AI Silent Defect Scanner — reproducible analysis targets.
# All analysis is deterministic (second layer of the two-tier design).
# Windows: PYTHONUTF8=1 is set per-target to avoid cp932 decode errors.
# No make? Run the commands under each target directly (see README "make が無い環境").

PY ?= python
export PYTHONUTF8 = 1

.PHONY: help reproduce gt figures footnote7b scan-mine

help:
	@echo "targets:"
	@echo "  make reproduce      # 3-way distribution (article Table in section 6) + naive Semgrep candidates (section 7)"
	@echo "  make gt             # (re)build results/gt.csv  (human-adjudication layer)"
	@echo "  make figures        # render results/figures/*.png"
	@echo "  make footnote7b     # reclassify the frozen 7B corpus raw7b/ (read-only, no Ollama)"
	@echo "  make scan-mine DIR=/path/to/your/repo   # try it on YOUR code"
	@echo "  (to REGENERATE raw7b/ from the model: python scripts/footnote_7b.py 3 -- destructive)"

reproduce:
	$(PY) scripts/classify_split.py
	$(PY) scripts/scan_and_count.py

gt:
	$(PY) scripts/build_gt.py

figures:
	$(PY) scripts/make_figures.py

# read-only: reclassify the frozen raw7b/ corpus. Does NOT call Ollama / does NOT
# overwrite raw7b/. To regenerate the corpus from the model, run scripts/footnote_7b.py
# directly (destructive — it re-samples raw7b/ and changes the frozen fixtures).
footnote7b:
	$(PY) scripts/reclassify_7b.py

scan-mine:
	$(PY) scripts/scan_mine.py $(DIR)
