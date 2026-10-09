# 研究拡張（この fork について）

本リポジトリは [ntt-dkiku/chaos-eater](https://github.com/ntt-dkiku/chaos-eater) の **研究用フォーク**（[@TeruFujita](https://github.com/TeruFujita) / 藤田直輝）です。

**提案実装は主に `pipeline_v0/`。** 公式の `chaos_eater/` 等は原則変更しないが、次の実行不能バグだけ例外で直している。

### 公式ツリーへの例外修正（2026-10-09）

| 変更 | 内容 |
|------|------|
| `chaos_eater/ce_tools/k8s/templates/k8s_pod_template.j2` | コンテナ名を `{{ pod_name }}-container` → 固定 `k8sapi` |
| `chaos_eater/ce_tools/k6/templates/k6_pod_template.j2` | 同上 → 固定 `k6` |
| `chaos_eater/hypothesis/steady_states/llm_agents/utils.py` | Pod 名が `-pod` 付与後も 63 文字以内になるよう切り詰め |

**理由:** 仮説フェーズの VaC 用 Pod が、長い steady state 名でコンテナ名 63 文字超 → apply 拒否 → 公式サイクルが完走不能。  
**触っていないもの:** LLM 配置・プロンプト・直しロジック。  
**実験の書き方:** この修正入りで測った値は「upstream と完全同一」とは書かず、「名前長修正あり」と明記する。比較実験では公式側・提案側とも同じ修正入りバイナリで揃える。

- C0 = 公式 ChaosEater サイクル（本 fork では上記修正入り）  
- C1–C4 = `python -m pipeline_v0 ...`  
- 評価プロトコル: 論文同一（NGINX / SOCKSHOP）。障害5ケース並べは主評価にしない。

詳細は [`pipeline_v0/README.md`](./pipeline_v0/README.md)。README 先頭にも研究用フォークである旨を記載しています。

## remotes

- `origin` = https://github.com/TeruFujita/chaos-eater.git（この fork）  
- `upstream` = https://github.com/ntt-dkiku/chaos-eater.git（公式）
