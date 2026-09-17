# ai-silent-defect-scanner

**「AIは失敗を握り潰す」と思って120本測ったら、話はもっと厄介だった——“握り潰し”は静的解析だけでは判定できない**（実測・Python/TS）。

ローカルLLM（Ollama + Qwen2.5-Coder、CPU・無料）に失敗経路が必然のI/Oを書かせ、失敗時の挙動を実測した再現キット。結論は **「候補は機械（sensitivity）／正当か握り潰しかの裁定は人（adjudication）」**。詳しくは [`ARTICLE.md`](ARTICLE.md)。

## 一言でいうと

- 同じ `return None` が、**役割上妥当な契約**にも、**バグを隠す握り潰し**にもなる。違いは docstring・コメント・仕様・呼び出し側の期待という**構文の外の意図**にあり、**コメントがあっても妥当とは限らない**（`fetch_json` が「非200なら None」とコメント付きで404/500/空を区別なく潰す例）。
- だから構文パターンを見る静的検出は**候補までは出せる**が、**正当か握り潰しかの最終判定はできない**。先行研究 [AIRA](https://arxiv.org/abs/2604.17587)（preprint）も、握り潰し系を決定的に検出しつつ「フラグ＝欠陥とは限らない・是正の前に必ず人手レビューが要る」と明記している。本リポはその残余を実物で具体化したもの。

## 二層再現（生成は非決定／解析は決定的）

- **第1層（生成・非決定・著者が1回）**：`raw/`（主実験120本＝失敗経路100＋純計算対照20）と `raw7b/`（7B補足30本）に全件無選別で凍結。条件は [`PROVENANCE.md`](PROVENANCE.md)。生成をやり直すと分布は変わる。
- **第2層（解析・決定的・あなたが再現）**：同じ150本に分類器・Semgrepルールを当てれば、記事と同じ分布・候補が出る。ただし **“正当か握り潰しか”の最終ラベルは著者の人手裁定**で [`results/gt.csv`](results/gt.csv) に透明化してある（そこは機械的に再導出できない＝それ自体が本記事のテーゼ）。

## クイックスタート

```bash
pip install -r requirements.lock.txt   # or: pip install semgrep ruff

make reproduce         # 失敗時挙動の分布（記事§6）＋ naive Semgrep 候補（§7）
make gt                # results/gt.csv を再生成（人手裁定層）
make figures           # results/figures/*.png
make scan-mine DIR=/path/to/your/repo   # あなたのコードで試す
```

### make が無い環境（Windows 等）

`make` の各ターゲットは素の Python でも動く（Windows は `PYTHONUTF8=1` を付ける）：

```bash
PYTHONUTF8=1 python scripts/classify_split.py     # 失敗経路の分布（§6・n=50/言語）
PYTHONUTF8=1 python scripts/scan_and_count.py     # naive Semgrep 候補（§7）
PYTHONUTF8=1 python scripts/build_gt.py           # results/gt.csv
PYTHONUTF8=1 python scripts/make_figures.py       # 図
PYTHONUTF8=1 python scripts/scan_mine.py DIR      # 自リポ試食
```

> `scan-mine` が挙げるのは**候補**であって判定ではありません。各候補を開き、関数の役割・呼び出し側契約・仕様を読んで初めて「正当なフォールバックか、握り潰しか」を裁定できます（＝人の仕事）。CI では `semgrep scan --error` で「候補あり」を exit 1 にできますが、それは**合否でなく“人が見るべき候補”の通知**です。

## リポ構成

```
ARTICLE.md         記事本文（Qiita技術版・落とし穴ログ=§8）
PROVENANCE.md      生成条件・ツールチェーン版・決定性の実測
tasks/tasks.json   12タスク（失敗経路I/O 5＋純計算対照1 ×2言語）
rules/             自作 naive Semgrep ルール（before）
scripts/           classify(3分類)/classify_split/scan_and_count/scan_mine/build_gt/make_figures/reclassify_7b/generate/footnote_7b/m0_probe
raw/ raw7b/        生成コーパス（固定同梱・raw7bは frozen。footnote_7b.py は破壊的=再サンプルする点に注意）
results/           gt.csv（人手裁定）・classification_summary.txt・footnote_7b.csv・figures/・版情報
```

### `gt.csv` の `subtype` 列（2026-09-17 追加）

`try` がある行でも空にせず、default を返す位置で分けた（読者 読者 の指摘に基づく）。Python は `ast`、TypeScript は tree-sitter（`pip install tree-sitter tree-sitter-typescript`）で、同じ定義。

| 値 | 意味 |
|---|---|
| `guard_default` | default return が **except handler の外**にある（handler の中には無い） |
| `handler_default` | default return が **handler の中だけ** |
| `both` | 両方にある |
| `bare` / `raise` | try が無い行の既存の分類 |
| 空 | try/catch はあるが default return が無い（raise / throw 系） |

「handler の外で default を返す」集合＝`guard_default ∪ both` は Python で 17 行（problematic_fallback 4・legit_fallback 2・proper 2・対照 9）、TypeScript で 11 行（`ts_get_item_s1-s9`・`ts_parse_int_s0/s5`）。

**TypeScript の注意**: `handling` 列は記事の数字を出した regex 分類のまま。tree-sitter の分類はそれと 58/60 で一致し、残り 2 行（`ts_load_config_s0/s2`＝末尾のデモ用ブロックのコメントだけの catch）は AST 側が `swallow_cand` と言う。これは naive Semgrep が拾って人が `false_positive` と裁定した 2 行そのもの。
TS の guard 集合 11 行は**人手裁定をしていない**（`ts_get_item_*` の `proper` は「catch が log か throw をする」という機械の判定であって、外側の default return を人が見た結果ではない）。TS の failure path に `problematic_fallback` が 0 件なのは「無い」ではなく「まだ開いていない」で、TS の recall は依然 0/0＝未定義。
**読者の再導出（2026-09-17・2 通目）で確定した 2 点**: ①記事の「候補 4 件」は 1 つの検出器の出力ではない＝Python の 2 件は `py-swallow-return-default`、TypeScript の 2 件は `ts-empty-catch`（`scripts/scan_and_count.py` の hits で確認）。厳格なアンカー（catch 本体が `return <default>` だけ）は、Python では log つきの 5 行、TypeScript では 9 行（全部 `console.error` → `return null/undefined` の 2 文・全部 proper）を除外する。②TypeScript 側は **対照群**として読む方が正確＝Python と共有する task は fetch_json・parse_int の 2 つだけで、Python の problematic 4 件が全部載る fetch_json は TS で 10/10 proper。TS の recall 0/0 は「未裁定」より「この task 標本の構成上、正例が空」が主因。guard 集合 11 行の未裁定 2 行（`ts_parse_int_s0/s5`）は著者の裁定待ち。

列を足したことで `has_raise` が TS の全行に入り、`throw` のみで catch が無い 4 行（`ts_parse_int_s4/s6/s7/s9`）は Python 側と同じ機械規則で `loud_fail` になった（それまでは `not_adjudicated` に含まれていた＝TS の内訳 31 proper / 27 not_adjudicated / 2 false_positive は 31 / 23 / 4 loud_fail / 2 に読み替え）。

## 数値（失敗経路 n=50/言語・qwen2.5-coder:1.5b）

| | try/except+proper | try/except default返し(候補) | try/except 不使用 |
|---|---|---|---|
| Python | 9 | 2（人手裁定→文書化済の正当） | 39（=raise14 / guard default返し4 / bare21） |
| TypeScript | 33 | 0 | 17 |

naive Semgrep の4候補は人手で全部が偽陽性（TS2）か文書化済の正当（Python2）。詳細と限界は [`ARTICLE.md`](ARTICLE.md) §7・§9・§12。

## ライセンス

本リポのコード・ルールは MIT（[`LICENSE`](LICENSE)）。Ollama=MIT／Qwen2.5-Coder=Apache-2.0／Semgrep CE=LGPL 2.1（自作ルールのみ同梱）。

## 利益相反（COI）と連絡先

筆者（**tauridev**）は AIコード監査サービスの出品者で、本リポの結論「最後は人が意図を裁定する」は事業上の立場に有利になり得ます。だからこそ生成物・分類器・人手裁定（gt.csv）・偽陽性・検出器の穴まで公開し、読者が検証できるようにしています。

- AIで作ったアプリの監査・修正 → https://coconala.com/services/4282365
- プロフィール → https://coconala.com/users/6153961 ／ https://getaxiom.dev

## 設計・検証の記録（Sumitsuke Lab）

このリポジトリの背景・検証環境・判定・最終検証日・失敗例は、Sumitsuke Lab の本家記事にまとめています。

- 生成 AI のコードは「失敗を握り潰す」のか——120 本を静的解析で当て、候補 4 本を人手で裁定した記録 → https://sumitsuke.jp/lab/ai-code-silent-fallback/
- 受託（生成 AI コード・外注コードの点検と修理・テキスト完結） → https://sumitsuke.jp/works/repair/
