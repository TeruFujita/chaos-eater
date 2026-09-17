#!/usr/bin/env bash
# C0 = official ChaosEater cycle. Do not use pipeline_v0 for baseline.
set -euo pipefail
echo "C0 baseline: start official ChaosEater (GUI localhost:3000 or official eval scripts)."
echo "Input must be examples/nginx or examples/sock-shop-2 — same as the paper."
echo "Then: make setup-sandbox   # or setup-standard"
echo "This script does not invent a second CE implementation."
exit 0
