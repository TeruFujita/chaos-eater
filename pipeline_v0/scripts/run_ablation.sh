#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
MODE="${1:-C4}"
CONFIG="${2:-pipeline_v0/configs/nginx.yaml}"
python -m pipeline_v0 --config "$CONFIG" --mode "$MODE"
