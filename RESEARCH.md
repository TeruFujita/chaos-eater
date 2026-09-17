# 研究拡張（この fork / 作業コピーについて）

本リポジトリは [ntt-dkiku/chaos-eater](https://github.com/ntt-dkiku/chaos-eater) をベースにする。  
**提案実装は `pipeline_v0/` のみ。** 公式の `chaos_eater/`・`examples/`・`k8s/`・`docker/` は原則変更しない。

- C0 = 公式 ChaosEater サイクル  
- C1–C4 = `python -m pipeline_v0 ...`  
- 評価プロトコル: 論文同一（NGINX / SOCKSHOP）。障害5ケース並べは主評価にしない。

詳細は `pipeline_v0/README.md`。

## GitHub に fork する

API トークンでは fork を作れなかった。ブラウザで公式を Fork したあと:

```text
git remote rename origin upstream
git remote add origin https://github.com/TeruFujita/chaos-eater.git
git push -u origin research/pipeline-v0
```

`upstream` = https://github.com/ntt-dkiku/chaos-eater.git  
`origin` = 自分の fork

