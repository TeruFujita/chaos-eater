"""Apply fixed Chaos Mesh fault YAML (LLM=None)."""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import yaml

from pipeline_v0.src.k8s_ops import apply_path, delete_path, ensure_namespace


def _duration_seconds(fault_path: Path, default: int = 35) -> int:
    try:
        data = yaml.safe_load(fault_path.read_text(encoding="utf-8")) or {}
        raw = (data.get("spec") or {}).get("duration") or ""
        if isinstance(raw, str) and raw.endswith("s"):
            return max(int(raw[:-1]) + 5, default)
        if isinstance(raw, str) and raw.endswith("m"):
            return max(int(raw[:-1]) * 60 + 5, default)
    except Exception:
        pass
    return default


def inject_faults(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    chaos_ns = config.get("chaos_ns") or "chaos-eater"
    ensure_namespace(chaos_ns)

    applied: list[dict[str, Any]] = []
    for rel in config.get("faults") or []:
        path = root / rel
        if not path.is_file():
            raise FileNotFoundError(f"fault yaml missing: {path}")
        # Clean previous apply so re-runs are deterministic.
        delete_path(path, namespace=chaos_ns)
        out = apply_path(path, namespace=chaos_ns)
        wait_s = _duration_seconds(path)
        time.sleep(wait_s)
        applied.append({"path": rel, "kubectl": out, "waited_s": wait_s})

    return {
        "status": "ok",
        "chaos_ns": chaos_ns,
        "applied": applied,
        "llm_calls": 0,
    }
