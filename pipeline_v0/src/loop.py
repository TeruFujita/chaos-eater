from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline_v0.src.deploy import deploy_example
from pipeline_v0.src.inject import inject_faults
from pipeline_v0.src.k8s_ops import cluster_reachable
from pipeline_v0.src.load_fixture import load_config
from pipeline_v0.src.metrics import append_event
from pipeline_v0.src.repair_llm import repair
from pipeline_v0.src.replan_rules import apply_rules
from pipeline_v0.src.verify_runner import run_verifies

# Inner-frame ablation. C0 = official ChaosEater (not this module).
MODES = {
    "C1": "fixed verify core; inject optional",
    "C2": "C1 + skip preprocess LLM accounting",
    "C3": "fixed verify + fixed inject (critical LLM-free path)",
    "C4": "C3 + repair Large on NG (needs API later)",
    "C5": "optional Small-then-Large repair",
}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="pipeline_v0: critical path = fixed verify/inject (LLM=None)"
    )
    parser.add_argument("--config", required=True, help="pipeline_v0/configs/*.yaml")
    parser.add_argument("--mode", default="C3", choices=sorted(MODES))
    parser.add_argument(
        "--execute",
        action="store_true",
        help="talk to the cluster (deploy/verify/inject)",
    )
    parser.add_argument(
        "--skip-repair",
        action="store_true",
        default=True,
        help="do not call repair LLM (default for critical path)",
    )
    parser.add_argument(
        "--with-repair",
        action="store_true",
        help="attempt repair LLM (needs API; not wired for execute yet)",
    )
    args = parser.parse_args()
    skip_repair = not args.with_repair

    root = _repo_root()
    cfg_path = Path(args.config)
    if not cfg_path.is_absolute():
        cfg_path = root / cfg_path
    config = load_config(cfg_path)
    out_dir = root / config.get("metrics", {}).get("out_dir", "pipeline_v0/results")

    summary: dict = {
        "mode": args.mode,
        "mode_meaning": MODES[args.mode],
        "example": config.get("example"),
        "example_dir": config.get("example_dir"),
        "execute": args.execute,
        "skip_repair": skip_repair,
        "llm_calls": 0,
        "note": "Critical claim: verification/inject without LLM invent.",
    }

    if not args.execute:
        summary["status"] = "dry-run"
        summary["would"] = [
            "deploy examples/* yaml",
            "pre-verify fixture scripts",
            "inject fixture Chaos Mesh YAML" if args.mode in {"C3", "C4", "C5"} else "skip inject",
            "post-verify",
            "repair skipped" if skip_repair else "repair Large (API)",
        ]
        append_event(out_dir, {"event": "pipeline_plan", "summary": summary})
        print(json.dumps(summary, ensure_ascii=True, indent=2))
        return

    ok, msg = cluster_reachable()
    if not ok:
        summary["status"] = "blocked"
        summary["error"] = f"cluster not reachable: {msg}"
        summary["hint"] = "Start Docker Desktop, then: make setup-sandbox (or setup-standard)"
        append_event(out_dir, {"event": "pipeline_blocked", "summary": summary})
        print(json.dumps(summary, ensure_ascii=True, indent=2))
        raise SystemExit(2)

    # --- critical path (LLM=None) ---
    summary["deploy"] = deploy_example(root, config)
    summary["pre_verify"] = run_verifies(root, config)

    do_inject = args.mode in {"C3", "C4", "C5"} or (
        args.mode in {"C1", "C2"} and bool(config.get("faults"))
    )
    if do_inject:
        summary["inject"] = inject_faults(root, config)
    else:
        summary["inject"] = {"status": "skipped", "llm_calls": 0}

    summary["post_verify"] = run_verifies(root, config)

    fail_log = ""
    if not summary["post_verify"].get("ok"):
        fail_log = json.dumps(summary["post_verify"], ensure_ascii=True)

    if skip_repair:
        summary["repair"] = {"status": "skipped", "reason": "critical path / --skip-repair", "llm_calls": 0}
        summary["replan"] = {"status": "skipped"}
    else:
        summary["repair"] = repair(config, fail_log=fail_log or "post_verify ok", execute=True)
        summary["replan"] = apply_rules(config, summary["repair"])

    # Success gate for phase1 critical demo: weak nginx should fail post_verify after inject.
    summary["critical_signal"] = {
        "pre_verify_ok": summary["pre_verify"].get("ok"),
        "post_verify_ok": summary["post_verify"].get("ok"),
        "expected_for_nginx_weak": "pre pass, post fail after pod-kill (restartPolicy Never)",
    }
    summary["status"] = "ok"
    append_event(out_dir, {"event": "pipeline_run", "summary": summary})
    print(json.dumps(summary, ensure_ascii=True, indent=2))

    # Non-zero if execute but post_verify still passes on nginx (unexpected for weak case).
    if config.get("example") == "nginx" and do_inject and summary["post_verify"].get("ok"):
        raise SystemExit(3)


if __name__ == "__main__":
    main()
