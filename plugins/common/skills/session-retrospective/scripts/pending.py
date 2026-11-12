"""Reminder for session-retrospective: days with sessions and no ledger line.

Meant for a session-start hook. Prints at most one ASCII line and ALWAYS exits 0, so it
can never block a session. It only reminds; it never runs the review.

Usage:
  python pending.py --project-dir DIR --ledger FILE [--since YYYY-MM-DD] [--window-days N]

Depends on the Claude Code JSONL transcript format. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path


def reviewed_days(ledger: Path) -> set[str]:
    if not ledger.is_file():
        return set()
    return set(re.findall(r"(?m)^- (\d{4}-\d{2}-\d{2}) ", ledger.read_text(encoding="utf-8")))


def days_with_sessions(project: Path, first: date, today: date) -> set[date]:
    cutoff = datetime.combine(first, datetime.min.time()).timestamp()
    days: set[date] = set()
    for path in project.glob("*.jsonl"):
        if path.stat().st_mtime < cutoff:
            continue
        with path.open(encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if '"type":"user"' not in line or '"isMeta":true' in line or '"tool_result"' in line:
                    continue
                try:
                    stamp = json.loads(line).get("timestamp")
                    day = datetime.fromisoformat(stamp.replace("Z", "+00:00")).astimezone().date()
                except (ValueError, AttributeError, json.JSONDecodeError):
                    continue
                if first <= day < today:
                    days.add(day)
    return days


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--project-dir", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--since", type=date.fromisoformat, help="ignore days before this date")
    parser.add_argument("--window-days", type=int, default=14)
    try:
        args = parser.parse_args()
        today = datetime.now().astimezone().date()
        first = max(args.since or date.min, today - timedelta(days=args.window_days))
        done = reviewed_days(args.ledger)
        pending = sorted(d.isoformat() for d in days_with_sessions(args.project_dir, first, today)
                         if d.isoformat() not in done)
        if pending:
            print(f"NOTICE retrospective: {len(pending)} day(s) with sessions and no review "
                  f"({', '.join(pending)}). Offer the review to the user; do not run it unasked.")
    except (Exception, SystemExit):  # a reminder must never get in the way of a session
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
