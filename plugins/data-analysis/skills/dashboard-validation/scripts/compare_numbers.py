"""Compare dashboard numbers with reproduced numbers, with explicit tolerance.

Input CSV columns (header required):
  number_id, dashboard_value, reproduced_value[, abs_tolerance][, rel_tolerance]

Tolerances default to the --abs / --rel options (both 0 by default, so set them).
A row matches if |diff| <= abs_tolerance OR |diff| <= rel_tolerance * |reproduced|.
Empty values are reported as MISSING, never treated as zero.

Prints one line per number (OK / DIVERGES / MISSING) and exits 1 if any row is not OK.
Standard library only.
"""

from __future__ import annotations

import argparse
import csv
import sys
from decimal import Decimal, InvalidOperation


def to_dec(text: str | None) -> Decimal | None:
    if text is None or not text.strip():
        return None
    try:
        return Decimal(text.strip().replace(",", ""))
    except InvalidOperation:
        return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_file")
    ap.add_argument("--abs", dest="abs_tol", default="0", help="default absolute tolerance")
    ap.add_argument("--rel", dest="rel_tol", default="0", help="default relative tolerance, e.g. 0.005")
    a = ap.parse_args(argv)
    default_abs, default_rel = Decimal(a.abs_tol), Decimal(a.rel_tol)
    bad = 0
    with open(a.csv_file, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            nid = row.get("number_id", "?")
            dash, rep = to_dec(row.get("dashboard_value")), to_dec(row.get("reproduced_value"))
            if dash is None or rep is None:
                print(f"MISSING  {nid}: a value is empty or not numeric")
                bad += 1
                continue
            abs_tol = to_dec(row.get("abs_tolerance"))
            rel_tol = to_dec(row.get("rel_tolerance"))
            abs_tol = default_abs if abs_tol is None else abs_tol
            rel_tol = default_rel if rel_tol is None else rel_tol
            diff = dash - rep
            ok = abs(diff) <= abs_tol or abs(diff) <= rel_tol * abs(rep)
            rel = f"{(diff / rep):.4%}" if rep else "n/a"
            print(f"{'OK      ' if ok else 'DIVERGES'} {nid}: dashboard={dash} reproduced={rep} diff={diff} ({rel})")
            bad += 0 if ok else 1
    print(f"{bad} number(s) need attention" if bad else "all numbers within tolerance")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
