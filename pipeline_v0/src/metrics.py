from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


def ensure_dir(path: str | Path) -> Path:
    out = Path(path)
    out.mkdir(parents=True, exist_ok=True)
    return out


def append_event(out_dir: str | Path, event: dict[str, Any]) -> Path:
    directory = ensure_dir(out_dir)
    path = directory / "metrics.jsonl"
    payload = {"ts": time.time(), **event}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return path
