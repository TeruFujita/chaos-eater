# 研究プロジェクト

研究で何が分かり、何が変わったかを成果物とともに残すためのリポジトリです。コードがまだなくても、テーマ検討や論文メモから始められます。

## 最初にすること

1. 研究室Organization `hisazumiken` への招待を承諾し、[テンプレート](https://github.com/hisazumiken/research-project-template)のページで **Use this template → Create a new repository** を選び、自分用のリポジトリを作る。所有者は `hisazumiken` を選ぶ。公開範囲はまず **Private** にする。
2. 作成したURLを教員に共有する。現在のOrg設定では研究室メンバーにRead権限があるため、非公開リポジトリも研究室内で閲覧・議論できる。自分に編集権限があることを確認する。権限はテンプレートの複製ではなくOrgと各リポジトリの設定で決まる。
3. このREADMEの「現在の研究」は書ける範囲で書き換える。仮テーマや問いは未定でよい。
4. [関心・調べたいことメモ](templates/theme-note.md)を `notes/theme.md` へコピーし、見た資料と素朴な疑問を並べる。初回にテーマを絞る必要はない。
5. 一つ成果物を残したら、**Issues → New issue → Weekly Review** から最初のレビューを作る。前回の欄は「初回」とする。

テンプレートが開けない場合は教員へ連絡する。GitHubの設定が間に合わなければ、まず手元のMarkdownで記録して後から移す。

Gitやエディタの準備がなくても、GitHubの **Add file → Create new file** で `notes/theme.md` などを作れる。[詳しい使い方](docs/workflow.md)と[記入例](examples/README.md)を参照。

## 現在の研究（自分の内容に置き換える）

- 仮のテーマ：Chaos Engineering（CE）自動化における **LLM の置き方（配置）とコスト** — 先行研究 ChaosEater を比較対象に、役割ごとの LLM をコード／テンプレに対応づけて置き換え、**直し（再構成）だけ大型 LLM** を残す構成の効きを測る
- 現在の問い：同じ題材（まず nginx、次に sock-shop）・同条件で、公式全部 LLM（C0）に対し、検証・注入を固定し直しだけ Large LLM（C4）にすると、**呼び出し・トークン・API$** はどこまで下がるか。クリティカルは「どの役割を切ると効くか」（全部一気置き換えだけでは言わない）
- 次に確かめたいこと：
  1. 安定 OpenAI **gpt-4o** で C0 nginx 一巡を完走し、コスト実測のベースを取る
  2. C4（固定 verify/inject ＋ repair のみ LLM）を接続し、同題材で C0 と比較表を作る
  3. 余力で途中条件（検証だけ固定など）や sock-shop へ拡張
- テーマ検討メモ：[notes/theme.md](notes/theme.md)
- 主な成果物：
  - [notes/status.md](notes/status.md)（進捗・条件定義の要約）
  - 実装の作業用リポジトリは別（ローカル `pipeline_v0`）。こちらには実験条件・結果・解釈を [experiments/](experiments/) に残す方針
  - 先行研究：ChaosEater — https://arxiv.org/abs/2501.11107

### いま切っているもの（スコープ外）

- 小型 LLM への置き換え・カスケード（今回は切る）
- ポスター用5障害ケース並べを主評価にすること（主評価は論文同一の nginx / sock-shop）

### 評価の立ち位置（短く）

| 役割 | 内容 |
|------|------|
| **ゲート** | CE 成功・非劣（完走・改善後検証）。成功だけを主スコアにしない |
| **主スコア** | 呼び出し回数・トークン・API$・時間、および「どの置換が効いたか」 |
| **公平性** | 検証・注入の固定は統制。直し方のゴールデンパッチ先出しはしない |

## 置き場所

| 場所 | 入れるもの |
|---|---|
| [literature/](literature/README.md) | 論文メモ、関連研究の比較表 |
| [notes/](notes/README.md) | テーマ、仮説、設計、議論、判断の経緯 |
| [experiments/](experiments/README.md) | 実験ごとの条件、実行方法、結果、解釈 |
| [src/](src/README.md) | 実装コード（必要になってから） |
| [presentations/](presentations/README.md) | 発表資料と指摘・修正内容 |
| [templates/](templates/README.md) | コピーして使うメモのひな形 |
| [examples/](examples/README.md) | 架空の記入例。自分の成果と混同しない |
| Issues | 作業・相談と、毎週のWeekly Review |

## 毎週の流れ

成果物を保存 → Weekly Review Issueで変化と根拠を整理 → 教員のレビュー／ゼミの議論 → 次の作業へ。

- **Weekly Reviewは全員毎週**。発表のない週も記録する。
- PRは機能・修正・実験など意味のある変更単位。週単位のPRにはせず、mergeを週末まで待たない。
- 教員のレビュー後、未完了課題の引継ぎを確認してWeekly IssueをCloseする。Closeはレビュー終了を表す。
- LLMによる下書きは使える。根拠とリンクを自分で確認し、自分の判断・分からない点を補う。[下書き用プロンプト](docs/weekly-draft-prompt.md)
- 締切、レビューの担当、発表順は授業で確認する。研究が止まる相談は次の発表まで待たない。

## 保存する前に

APIキー、パスワード、被験者の個人情報はコミットしない。論文PDFはまず原典へのリンクと自分のメモを共有する。大きなデータや共有制限のある資料は、許可された保存先へのリンクと取得・再現手順を記録する。

調べ方に迷ったら、[前期資料を見ながら調査と議論を始めるガイド](docs/survey-start.md)を使えます。ネタがあればLLMによる俯瞰調査から始め、未定なら資料の閲覧と疑問の列挙から始めます。
