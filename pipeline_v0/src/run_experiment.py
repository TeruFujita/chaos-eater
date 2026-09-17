"""Wrap official ChaosEater experiment execution later.

Phase 1 will call chaos_eater.experiment.experimenter.Experimenter.run
and/or ce_tools. This module only records the intended call.
"""
from __future__ import annotations

from typing import Any


def run_fixed_experiment(config: dict[str, Any], *, execute: bool = False) -> dict[str, Any]:
    faults = config.get("faults") or []
    if not execute:
        return {
            "status": "dry-run",
            "would_apply": faults,
            "note": "Official Experimenter.run / Chaos Mesh apply is not wired yet.",
        }
    raise NotImplementedError(
        "Execute path: apply fixture YAML via chaos_eater.ce_tools, then wait for workflow."
    )
