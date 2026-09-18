"""Deploy official example manifests without LLM / invent."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from pipeline_v0.src.k8s_ops import apply_path, ensure_namespace, wait_for_pod


def deploy_example(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    example_dir = root / config["example_dir"]
    if not example_dir.is_dir():
        raise FileNotFoundError(f"example_dir not found: {example_dir}")

    app_ns = config.get("app_ns") or config.get("namespace") or "default"
    ensure_namespace(app_ns)

    applied: list[str] = []
    # Prefer yaml next to skaffold; skip skaffold.yaml itself.
    for path in sorted(example_dir.glob("*.yaml")):
        if path.name == "skaffold.yaml":
            continue
        applied.append(str(path.relative_to(root)))
        apply_path(path)

    example = config.get("example")
    waited = None
    if example == "nginx":
        wait_for_pod("example-pod", app_ns, timeout_s=120)
        waited = {"pod": "example-pod", "namespace": app_ns}
    # sock-shop-2: many resources; caller may wait via verify duration instead.

    return {
        "status": "ok",
        "example_dir": str(example_dir.relative_to(root)),
        "app_ns": app_ns,
        "applied": applied,
        "waited": waited,
        "llm_calls": 0,
    }
