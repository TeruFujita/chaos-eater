# 研究拡張（この fork について）

本リポジトリは [ntt-dkiku/chaos-eater](https://github.com/ntt-dkiku/chaos-eater) の **研究用フォーク**（[@TeruFujita](https://github.com/TeruFujita) / 藤田直輝）です。

**提案実装は `pipeline_v0/` のみ。** 公式の `chaos_eater/`・`examples/`・`k8s/`・`docker/` は原則変更しない。

- C0 = 公式 ChaosEater サイクル  
- C1–C4 = `python -m pipeline_v0 ...`  
- 評価プロトコル: 論文同一（NGINX / SOCKSHOP）。障害5ケース並べは主評価にしない。

詳細は [`pipeline_v0/README.md`](./pipeline_v0/README.md)。README 先頭にも研究用フォークである旨を記載しています。

## remotes

- `origin` = https://github.com/TeruFujita/chaos-eater.git（この fork）  
- `upstream` = https://github.com/ntt-dkiku/chaos-eater.git（公式）
