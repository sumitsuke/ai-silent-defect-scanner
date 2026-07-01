"""Render figures from the measured numbers (article section 6).
English labels (portable fonts). Output: results/figures/fig1_handling_by_language.png
Numbers are the measured failure-prone distribution (n=50/lang); reproduce via classify.py."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("results/figures", exist_ok=True)

# Measured, failure-prone tasks only (n=50 per language). See results/classification_summary.txt.
# Python no_try_except (39) is split: raise 14 / guard-default 4 / bare 21.
langs = ["Python", "TypeScript"]
segments = [
    ("try/except: proper (log or re-raise)", [9, 33], "#2e7d32"),
    ("try/except: default-return (candidate)", [2, 0], "#c62828"),
    ("no try/except: raise (loud fail)",       [14, 0], "#1565c0"),
    ("no try/except: guard default-return",    [4, 0], "#ef6c00"),
    ("no try/except: bare (propagates)",       [21, 17], "#9e9e9e"),
]

fig, ax = plt.subplots(figsize=(8.4, 4.8))
bottoms = [0, 0]
for label, vals, color in segments:
    ax.bar(langs, vals, bottom=bottoms, label=label, color=color, edgecolor="white", width=0.55)
    for i, v in enumerate(vals):
        if v:
            ax.text(i, bottoms[i] + v / 2, str(v), ha="center", va="center",
                    color="white", fontsize=10, fontweight="bold")
    bottoms = [b + v for b, v in zip(bottoms, vals)]

ax.set_ylabel("generations (n = 50 per language)")
ax.set_title("How Qwen2.5-Coder 1.5B handles failure on failure-prone I/O tasks\n"
             "(measured; candidates are not verdicts — see article section 9)", fontsize=11)
ax.set_ylim(0, 55)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=1, fontsize=8, frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
out = "results/figures/fig1_handling_by_language.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"wrote {out}")
