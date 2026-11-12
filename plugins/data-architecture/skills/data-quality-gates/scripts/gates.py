"""Minimal block/warn gate runner.

Define gates as functions returning (passed, message); register with a severity.
Exit code 1 if any blocking gate fails; warnings are printed and recorded.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from typing import Callable

BLOCK, WARN = "block", "warn"


@dataclass(frozen=True)
class GateResult:
    gate: str
    severity: str
    passed: bool
    message: str

    @property
    def state(self) -> str:
        return "pass" if self.passed else self.severity


def run_gates(gates: list[tuple[str, str, Callable[[], tuple[bool, str]]]]) -> list[GateResult]:
    results = []
    for name, severity, fn in gates:
        try:
            passed, msg = fn()
        except Exception as exc:  # a crashing gate is a failing gate
            passed, msg = False, f"gate raised {type(exc).__name__}: {exc}"
        results.append(GateResult(name, severity, passed, msg))
    return results


def report(results: list[GateResult], manifest_path: str | None = None) -> int:
    for r in results:
        label = {"pass": "OK", "warn": "WARN", "block": "ERROR"}[r.state]
        print(f"{label}: {r.gate} - {r.message}")
    if manifest_path:
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump([asdict(r) | {"state": r.state} for r in results], f, indent=2)
    return 1 if any(r.state == BLOCK for r in results) else 0


if __name__ == "__main__":
    demo = [
        ("source fresh", BLOCK, lambda: (True, "loaded 2h ago, threshold 24h")),
        ("volume in band", WARN, lambda: (False, "rows -38% vs 28-day median")),
    ]
    sys.exit(report(run_gates(demo)))
