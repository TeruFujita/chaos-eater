#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
CONFIG="${1:-pipeline_v0/configs/nginx.yaml}"
MODE="${2:-C3}"
python -m pipeline_v0 --config "$CONFIG" --mode "$MODE" --execute
