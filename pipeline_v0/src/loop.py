from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline_v0.src.load_fixture import load_config
from pipeline_v0.src.metrics import append_event
from pipeline_v0.src.repair_llm import repair
from pipeline_v0.src.replan_rules import apply_rules
from pipeline_v0.src.run_experiment import run_fixed_experiment

# Inner-frame ablation (evaluation protocol). C0 is the official binary, not this module.
MODES = {
    "C1": "fixed verify; inject may still be open; repair Large on NG",
    "C2": "C1 + skip preprocess LLM accounting",
    "C3": "C1 + fixed inject YAML",
    "C4": "proposal: skip invent, fixed verify+inject, repair Large on NG",
    "C5": "optional Small-then-Large repair (off unless measured cheaper)",
}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(description="pipeline_v0 research loop (fixture-based)")
    parser.add_argument("--config", required=True, help="path to pipeline_v0/configs/*.yaml")
    parser.add_argument("--mode", default="C4", choices=sorted(MODES))
    parser.add_argument(
        "--execute",
        action="store_true",
        help="actually call cluster/LLM (not implemented in skeleton)",
    )
    args = parser.parse_args()

    root = _repo_root()
    cfg_path = Path(args.config)
    if not cfg_path.is_absolute():
        cfg_path = root / cfg_path
    config = load_config(cfg_path)
    out_dir = config.get("metrics", {}).get("out_dir", "pipeline_v0/results")

    steps = [
        "deploy (official skaffold / examples; not invent)",
        "pre-verify (fixture scripts, LLM=None)",
        "inject (fixture Chaos Mesh YAML in C3/C4)",
        "post-verify (same scripts)",
        "repair Large LLM on NG only",
        "replan_rules then re-verify",
    ]
    if args.mode in {"C1", "C2"}:
        steps[2] = "inject (optional / not required for C1 core claim)"

    experiment = run_fixed_experiment(config, execute=args.execute)
    repair_result = repair(config, fail_log="dry-run: verify NG not executed", execute=args.execute)
    replan = apply_rules(config, repair_result)

    summary = {
        "mode": args.mode,
        "mode_meaning": MODES[args.mode],
        "example": config.get("example"),
        "example_dir": config.get("example_dir"),
        "execute": args.execute,
        "steps": steps,
        "experiment": experiment,
        "repair": repair_result,
        "replan": replan,
        "llm_calls_planned": 0 if args.mode in {"C1", "C2", "C3", "C4"} and not args.execute else None,
        "note": "C0 must be launched via official ChaosEater, not this module.",
    }
    append_event(root / out_dir, {"event": "pipeline_plan", "summary": summary})
    print(json.dumps(summary, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
