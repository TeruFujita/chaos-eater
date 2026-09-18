# pipeline_v0 — 研究用パイプライン（提案側）

ChaosEater 公式ツリーは触らない。検証環境・examples・`ce_tools` は公式のまま使い、**invent（仮説・VaC・計画の LLM 生成）だけを fixture で差し替える**。

## 入口の分け方

| 条件 | 起動 | 中身 |
|------|------|------|
| **C0**（ベースライン） | 公式 GUI / 公式 CE サイクル | 厚い LLM invent あり |
| **C3**（クリティカル・今ここ） | `python -m pipeline_v0 --config ... --mode C3 --execute` | **LLMなし** deploy→verify→inject→verify |
| **C4** | 同上 + `--with-repair` | C3 + repair Large（**API後回し**） |
| **C0** | 公式 GUI / 公式 CE | 厚い invent |

公式コードに invent ON/OFF スイッチは埋め込まない。切り替えるのは **起動するパイプライン** だけ。

## クリティカル実装（API不要）

主張の本命は「検証・注入を invent せず固定できる」。repair（API）は後でよい。

```text
# 1) クラスタ用意（Docker Desktop 起動後）
make setup-sandbox

# 2) LLMなしクリティカル経路（nginx 弱い設定）
python -m pipeline_v0 --config pipeline_v0/configs/nginx.yaml --mode C3 --execute
# 期待: pre_verify=pass, pod-kill 後 post_verify=fail（restartPolicy: Never）
```

Windows: `pipeline_v0/scripts/run_critical.ps1`

## カンニング回避ルール（重要）

たとえ話: **採点基準・問題文を先に決めるのは実験。模範解答を最初から出すのは不正。**

| やってよい（問題定義） | やってはいけない（模範解答） |
|------------------------|------------------------------|
| 調べ方の固定（verify スクリプト） | 直し方の固定（成功パッチ YAML を fixture に置く） |
| 壊し方の固定（Chaos Mesh YAML） | 公式評価の成功マニフェストをコピーして「直った」ことにする |
| 論文と同じ弱い入力（examples） | 自分だけ易しい問題／相手だけ高いモデル |

**ルール（この研究で固定）:**

1. **直し（repair）は必ず AI（API）。** 答えのマニフェストを先に書かない  
2. **調べ方・壊し方は固定してよい。** コスト削減の本命。論文には「問題定義であり発明力比較ではない」と書く  
3. 査読で疑われたら: 両構成とも同じ固定 verify/inject を使い、差は LLM 配置だけ、と説明する  
4. 調べ方・壊し方まで全部 AI に戻すと、クリティカルな安さの主張は弱くなる → 本線は「直しだけ AI」

関連: リポジトリ外の Obsidian `評価の公平性-カンニング回避`

## 前提（評価）

- 入力の正: `examples/nginx` / `examples/sock-shop-2`
- 成功はゲート。主スコアは呼び出し回数・コスト・「どの置換が効いたか」
- **修正 YAML のハードコード禁止（上記ルール）**
- repair / カスケードは後回し（repair は API 接続後）

## ディレクトリ

```text
pipeline_v0/
  configs/          例ごとの設定
  fixtures/         固定 verify / Chaos Mesh / plan
  src/              deploy, verify, inject, loop, ...
  scripts/          run_critical / C0 / ablation
  results/          計測出力（git 管理しない）
```

## いま動くこと / まだなこと

- **いま:** C3 クリティカル経路の実装（クラスタが上がっていれば `--execute`）
- **まだ:** Chaos Mesh 未導入時のエラーは明示終了。repair API 接続は未実装

環境は公式どおり `make setup-sandbox`（または standard）を先に通す。
