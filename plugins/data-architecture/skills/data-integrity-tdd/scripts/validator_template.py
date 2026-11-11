"""Data validator template: copy, rename to NN_validate_<topic>.py and fill the contract.

Prints one ASCII line per check and exits 1 when any ERROR exists.
Requires pandas, which is not in the Python standard library.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class Check:
    level: str  # "OK" | "ERROR" | "WARN"
    name: str
    detail: str


def check_unique_grain(df: pd.DataFrame, key: list[str]) -> Check:
    dup = int(df.duplicated(key).sum())
    return Check("OK" if dup == 0 else "ERROR", "unique grain", f"{dup} duplicates on {key}")


def check_count(df: pd.DataFrame, source_rows: int) -> Check:
    ok = len(df) == source_rows
    return Check("OK" if ok else "ERROR", "count vs source", f"{len(df)} vs {source_rows}")


def check_window(df: pd.DataFrame, column: str, start: str, end: str) -> Check:
    ts = pd.to_datetime(df[column], utc=True)
    inside = bool(((ts >= pd.Timestamp(start, tz="UTC")) & (ts < pd.Timestamp(end, tz="UTC"))).all())
    return Check("OK" if inside else "ERROR", "half-open window (UTC)", f"[{start}, {end})")


def check_nulls(df: pd.DataFrame, columns: list[str], sentinels: tuple = ("NULL", "", "-1")) -> list[Check]:
    out = []
    for col in columns:
        nulls = int(df[col].isna().sum())
        sent = int(df[col].astype(str).isin(sentinels).sum())
        level = "OK" if nulls == 0 and sent == 0 else "WARN"
        out.append(Check(level, f"nulls/sentinels {col}", f"{nulls} null, {sent} sentinel"))
    return out


def check_total(actual: float, expected: float, tolerance: float, name: str) -> Check:
    ok = abs(actual - expected) <= tolerance
    return Check("OK" if ok else "ERROR", name, f"{actual:.2f} vs {expected:.2f} (tol {tolerance})")


def run(checks: list[Check]) -> int:
    for c in checks:
        print(f"{c.level}: {c.name} - {c.detail}")
    return 1 if any(c.level == "ERROR" for c in checks) else 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("csv")
    p.add_argument("--key", nargs="+", required=True)
    p.add_argument("--source-rows", type=int, required=True)
    p.add_argument("--date-col", required=True)
    p.add_argument("--start", required=True)
    p.add_argument("--end", required=True)
    p.add_argument("--critical", nargs="*", default=[])
    a = p.parse_args()
    df = pd.read_csv(a.csv, dtype={k: str for k in a.key})
    checks = [
        check_unique_grain(df, a.key),
        check_count(df, a.source_rows),
        check_window(df, a.date_col, a.start, a.end),
        *check_nulls(df, a.critical),
    ]
    return run(checks)


if __name__ == "__main__":
    sys.exit(main())
