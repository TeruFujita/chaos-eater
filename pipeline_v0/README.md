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

## 前提（評価）

- 入力の正: `examples/nginx` / `examples/sock-shop-2`
- 成功はゲート。主スコアは呼び出し回数・コスト・「どの置換が効いたか」
- 修正 YAML のハードコード禁止
- repair / カスケードは後回し

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
