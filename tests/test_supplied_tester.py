from __future__ import annotations

import sys
import threading
from pathlib import Path


def test_supplied_tester_passes_against_maintained_api():
    repo_root = Path(__file__).resolve().parents[1]
    if not hasattr(threading.Thread, "isAlive"):
        threading.Thread.isAlive = threading.Thread.is_alive  # type: ignore[attr-defined]

    original_path = sys.path[:]
    try:
        sys.path.insert(0, str(repo_root / "assignment"))
        sys.path.insert(0, str(repo_root))
        namespace = {"__name__": "__supplied_hw5_tester__"}
        exec((repo_root / "hw5.py").read_text(encoding="utf-8"), namespace)
        exec((repo_root / "assignment" / "hw5_tester.py").read_text(encoding="utf-8"), namespace)
    finally:
        sys.path[:] = original_path

    assert namespace["test_results"] == ["0"]
