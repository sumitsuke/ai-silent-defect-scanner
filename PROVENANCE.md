# PROVENANCE — 生成条件と再現メタデータ

本リポジトリの `raw/`（主実験120本）・`raw7b/`（7B補足30本）の生成条件と、解析側ツールチェーンの版を記録する。
**二層再現の原則**：生成（第1層）は非決定的で著者が1回だけ実行し固定同梱。読者が再現するのは決定的な解析側（第2層＝分類器・Semgrep・集計）。生成をやり直すと分布は変わる。

## 生成（第1層・非決定・著者1回）

| 項目 | 値 |
|---|---|
| 生成エンジン | Ollama（ローカル・CPU） |
| モデル（主実験） | `qwen2.5-coder:1.5b`（Apache-2.0） |
| モデル（補足脚注） | `qwen2.5-coder:7b`（Apache-2.0） |
| 量子化 | Ollama 既定（Q4_K_M 相当のGGUF） |
| temperature | 0.7（分布を出すため。temp0 は決定的＝下記M0参照） |
| top_k / top_p | 40 / 0.9 |
| num_ctx / num_predict | 2048 / 384 |
| num_thread | 4（固定） |
| seed | 各タスク 0–9（主実験 N=10）／7B は 0–2（N=3） |
| タスク数 | 12（Python6＋TypeScript6。各 失敗経路I/O 5＋純計算対照 1） |
| 生成本数 | 主実験 12×10=120（失敗経路100＋対照20）／7B 失敗経路10×3=30／**計150** |
| OS | Windows 11（`PYTHONUTF8=1` で解析実行） |
| 生成日 | 2026-07-01 |

プロンプトは中立（「エラー処理を書け」等の誘導なし）。`tasks/tasks.json` に凍結。`raw/` は全件無選別で凍結（seed連番・欠番なし・数値目的の改変なし）。

## 決定性の実測（M0）

`scripts/m0_probe.py` 実測（`results/m0_probe_result.txt`）：
- temperature 0・num_thread 4 固定で **同一 seed 2回生成が byte 完全一致**（sha `a7d6c991ae5fc2eb`）。
- ＝この環境では llama.cpp PR#16016「CPU is already deterministic」が確認された。分布を測るには temp>0 が必要（seed 軸に変動を入れる）ため主実験は temp0.7。
- 所要：生成 cold 45.1s / warm 2.5s（1.5B・256トークン）／ruff 0.06s／semgrep 2.54s/ファイル。

## 解析（第2層・決定的・読者が再現）

| ツール | 版 |
|---|---|
| semgrep | 1.168.0（CE・LGPL 2.1） |
| ruff | 0.15.12 |
| node | v24.14.0 |
| python | 3.12.10 |

固定依存：`requirements.lock.txt`（解析側67パッケージ）。実行時は `PYTHONUTF8=1`（Windows cp932 回避）。

## ライセンス（一次確認 2026-07-01）

- 本リポジトリのコード・ルール：MIT（`LICENSE`）。
- Ollama：MIT ／ Qwen2.5-Coder：Apache-2.0（0.5/1.5/7/14/32B。3BのみQwen-Research・72B無し） ／ Semgrep CE エンジン：LGPL 2.1（自作ルールのみ同梱）。
