# 公式 sock-shop：Phase 0 失敗（2026-10-14）

## 条件
- 経路：公式 GUI（example#3 Sock shop）
- モデル：openai/gpt-4o-2024-08-06（予定どおり開始）
- 指示：実験1分以内、k6 URL 制約（公式例どおり）

## 結果
- **failed**（AI の仮説・直しの前）
- skaffold：`1/14 deployment(s) failed`
- 直接エラー：`weaveworksdemos/front-end:0.3.12 can't be pulled`

## 解釈
- 論文の「障害注入後に検証が落ちる／直しが効く」系の結果ではない
- Docker Hub 上にタグは存在する。個人環境（Docker Desktop + sandbox 入れ子）での取得失敗・DNS タイムアウト・その後の Desktop 過負荷が主因とみる
- **個人ノートPCだと sock-shop 規模は過負荷になりやすい**、と記録する

## 論文手順との関係
| やったこと | 論文から離れているか |
|---|---|
| 公式 GUI・同じ題材・同じ指示で回そうとした | 離れていない（再現のつもり） |
| front-end 等を事前 pull → kind に load | **運用回避**。論文本文の手法変更ではない。比較メモに「実行基盤の前処理」と注記する |
| 調べ・壊し固定／直しだけAI（別系統） | 研究側の意図した変更。今回の失敗原因ではない |

## 次
- イメージ事前 load 済みの状態で新規実行し直し
- mongo 等の巨大イメージの無理な事前 load は Desktop を落とすので避ける
