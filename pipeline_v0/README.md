# pipeline_v0 — 研究用パイプライン（提案側）

ChaosEater 公式ツリーは触らない。検証環境・examples・`ce_tools` は公式のまま使い、**invent（仮説・VaC・計画の LLM 生成）だけを fixture で差し替える**。

## 入口の分け方

| 条件 | 起動 | 中身 |
|------|------|------|
| **C0**（ベースライン） | 公式 GUI / 公式 CE サイクル | 厚い LLM invent あり |
| **C1–C4**（提案） | `python -m pipeline_v0 --config pipeline_v0/configs/nginx.yaml --mode C4` | 固定 verify / 固定 inject。repair だけ Large LLM |

公式コードに invent ON/OFF スイッチは埋め込まない。切り替えるのは **起動するパイプライン** だけ。

## 前提（評価）

- 入力の正: `examples/nginx` / `examples/sock-shop-2`（論文の弱い設定）
- 成功はゲート（CE 完走・検証達成）。主スコアは呼び出し回数・コスト・「どの置換が効いたか」
- 修正結果 YAML を fixture に置いて勝たせない
- Small→Large カスケードは実測で得なら。最初は載せない

## ディレクトリ

```text
pipeline_v0/
  configs/          例ごとの設定
  fixtures/         固定 verify / Chaos Mesh / plan
  src/              ループ・metrics・repair ラッパ
  scripts/          C0 / ablation 起動
  results/          計測出力（git 管理しない）
```

## いま動くこと / まだなこと

- **いま:** 設定と fixture の読み込み、モードごとの工程表示、dry-run
- **まだ:** 公式 `Experimenter.run` / `ReconfigurationAgent` への接続（フェーズ1–2）

環境は公式どおり `make setup-sandbox`（または standard）を先に通す。
