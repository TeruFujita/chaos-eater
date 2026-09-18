"""Run fixed verify scripts (LLM=None)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any


def run_verifies(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    scripts = config.get("verify") or []
    results: list[dict[str, Any]] = []
    all_ok = True
    for rel in scripts:
        path = root / rel
        if not path.is_file():
            raise FileNotFoundError(f"verify script missing: {path}")
        proc = subprocess.run(
            [sys.executable, str(path)],
            cwd=str(root),
            capture_output=True,
            text=True,
        )
        ok = proc.returncode == 0
        all_ok = all_ok and ok
        results.append(
            {
                "script": rel,
                "ok": ok,
                "returncode": proc.returncode,
                "stdout": (proc.stdout or "")[-2000:],
                "stderr": (proc.stderr or "")[-1000:],
            }
        )
    return {
        "status": "pass" if all_ok else "fail",
        "ok": all_ok,
        "results": results,
        "llm_calls": 0,
    }
