"""Call official ReconfigurationAgent on verify NG only.

Never load a golden patched manifest from fixtures.
"""
from __future__ import annotations

from typing import Any


def repair(config: dict[str, Any], fail_log: str, *, execute: bool = False) -> dict[str, Any]:
    repair_cfg = config.get("repair") or {}
    if not repair_cfg.get("enabled", True):
        return {"status": "skipped", "reason": "repair disabled"}
    if (repair_cfg.get("model_size") or "large").lower() != "large":
        raise ValueError("v0 main path: repair must be Large LLM only (cascade is optional later)")
    if not execute:
        return {
            "status": "dry-run",
            "agent": repair_cfg.get("agent"),
            "model_size": "large",
            "fail_log_preview": fail_log[:200],
            "note": "Will import ReconfigurationAgent; must not hardcode replicas/Deployment YAML.",
        }
    raise NotImplementedError(
        "Execute path: instantiate ReconfigurationAgent and apply create/replace/delete."
    )
