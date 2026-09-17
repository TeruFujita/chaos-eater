"""Deterministic selector/verify updates after repair (e.g. Pod -> Deployment).

This is not LLM. Nginx case: after Deployment exists, verify Ready instead of a Pod name.
"""
from __future__ import annotations

from typing import Any


def apply_rules(config: dict[str, Any], repair_result: dict[str, Any]) -> dict[str, Any]:
    example = config.get("example")
    if example == "nginx":
        return {
            "verify_hint": "If Pod was replaced by Deployment, switch verify to Deployment Ready.",
            "fault_hint": "Keep labelSelectors app=example.",
            "applied": False,
            "repair_status": repair_result.get("status"),
        }
    if example == "sock-shop-2":
        return {
            "verify_hint": "front-end Deployment Ready; desired replicas may have changed.",
            "fault_hint": "Keep labelSelectors name=front-end.",
            "applied": False,
            "repair_status": repair_result.get("status"),
        }
    return {"applied": False, "repair_status": repair_result.get("status")}
