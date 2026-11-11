"""Skeleton for a recurring job entry point with explicit run modes.

Read-only modes: plan, preflight, check-sources. Writing modes: run, retry (need --confirm).
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date

READ_ONLY = {"plan", "preflight", "check-sources"}
WRITING = {"run", "retry"}

log = logging.getLogger("job")


def plan(ref: date) -> int:
    log.info("OK plan ref=%s: would read sources X, Y and publish to <destination>", ref)
    return 0


def preflight(ref: date) -> int:
    log.info("OK preflight ref=%s: credentials present, destination reachable", ref)
    return 0


def check_sources(ref: date) -> int:
    log.info("OK check-sources ref=%s: inputs complete for the window", ref)
    return 0


def run(ref: date, *, retry: bool) -> int:
    # acquire -> normalize -> rules -> validate (block/warn) -> write .partial -> atomic replace
    log.info("OK %s ref=%s", "retry" if retry else "run", ref)
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=sorted(READ_ONLY | WRITING))
    p.add_argument("--ref-date", type=date.fromisoformat, required=True,
                   help="reference date; never taken silently from the clock")
    p.add_argument("--confirm", action="store_true", help="required for writing modes")
    a = p.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if a.mode in WRITING and not a.confirm:
        log.error("ERROR mode %s writes data; rerun with --confirm", a.mode)
        return 2
    handlers = {"plan": plan, "preflight": preflight, "check-sources": check_sources}
    if a.mode in handlers:
        return handlers[a.mode](a.ref_date)
    return run(a.ref_date, retry=a.mode == "retry")


if __name__ == "__main__":
    sys.exit(main())
