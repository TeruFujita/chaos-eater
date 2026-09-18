"""Minimal kubectl helpers for pipeline_v0 (no LLM)."""
from __future__ import annotations

import shutil
import subprocess
import time
from pathlib import Path
from typing import Optional


class K8sError(RuntimeError):
    pass


def have_kubectl() -> bool:
    return shutil.which("kubectl") is not None


def run_kubectl(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    if not have_kubectl():
        raise K8sError("kubectl not found on PATH")
    cmd = ["kubectl", *args]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if check and proc.returncode != 0:
        raise K8sError(
            f"kubectl {' '.join(args)} failed ({proc.returncode}): {proc.stderr.strip() or proc.stdout.strip()}"
        )
    return proc


def cluster_reachable() -> tuple[bool, str]:
    if not have_kubectl():
        return False, "kubectl not found"
    proc = run_kubectl(["cluster-info"], check=False)
    if proc.returncode != 0:
        return False, (proc.stderr or proc.stdout or "cluster unreachable").strip()[:300]
    return True, "ok"


def ensure_namespace(name: str) -> None:
    proc = run_kubectl(["get", "ns", name], check=False)
    if proc.returncode != 0:
        run_kubectl(["create", "namespace", name])


def apply_path(path: Path, *, namespace: Optional[str] = None) -> str:
    args = ["apply", "-f", str(path)]
    if namespace:
        args.extend(["-n", namespace])
    proc = run_kubectl(args)
    return proc.stdout.strip()


def delete_path(path: Path, *, namespace: Optional[str] = None) -> str:
    args = ["delete", "-f", str(path), "--ignore-not-found"]
    if namespace:
        args.extend(["-n", namespace])
    proc = run_kubectl(args, check=False)
    return (proc.stdout or proc.stderr or "").strip()


def wait_for_pod(
    name: str,
    namespace: str,
    *,
    timeout_s: int = 120,
    phase: str = "Running",
) -> None:
    deadline = time.time() + timeout_s
    last = ""
    while time.time() < deadline:
        proc = run_kubectl(
            ["get", "pod", name, "-n", namespace, "-o", "jsonpath={.status.phase}"],
            check=False,
        )
        last = (proc.stdout or "").strip()
        if proc.returncode == 0 and last == phase:
            return
        time.sleep(2)
    raise K8sError(f"timeout waiting for pod/{name} in {namespace} to be {phase} (last={last!r})")
