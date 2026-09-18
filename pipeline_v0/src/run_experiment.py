"""Wrap / legacy name — critical path uses inject.py + verify_runner.py directly."""
from __future__ import annotations

from typing import Any


def run_fixed_experiment(config: dict[str, Any], *, execute: bool = False) -> dict[str, Any]:
    faults = config.get("faults") or []
    if not execute:
        return {
            "status": "dry-run",
            "would_apply": faults,
            "note": "Use pipeline_v0 loop --execute (inject_faults).",
        }
    return {
        "status": "delegated",
        "note": "loop.py calls inject_faults / run_verifies directly.",
        "faults": faults,
    }
