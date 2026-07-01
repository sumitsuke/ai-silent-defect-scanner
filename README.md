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
