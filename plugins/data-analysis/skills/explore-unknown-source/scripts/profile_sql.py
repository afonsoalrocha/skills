"""Write SQL that profiles fields and tests candidate links. Prints SQL; runs nothing.

profile   one row per field: rows, filled, distinct, a few example values.
          --table T  --columns a,b,c | --columns-file F
          [--dialect duckdb|postgres|spark|mysql] [--date-column D --start S --end E]
          [--block N] [--examples K] [--width W] [--pii-pattern REGEX] [--keep-pii]
key-test  coverage, null keys and duplicate keys on both sides of a candidate link.
          --left A --left-key KA --right B --right-key KB

Fields whose names match the personal-data pattern are excluded and listed in a comment.
Defaults: 10 fields per query, 3 examples, 40 characters. Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys

PERSONAL = (
    r"(name|e_?mail|phone|mobile|document|tax_?id|ssn|passport|address|street|zip|"
    r"postal|birth|card|iban|account_?number|ip_?addr|payload|password|token|secret)"
)
IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_.$]*$")
TEXT_TYPE = {"duckdb": "VARCHAR", "postgres": "TEXT", "spark": "STRING", "mysql": "CHAR"}


def q(name: str) -> str:
    if not IDENT.match(name):
        raise SystemExit(f"ERROR: unsafe identifier {name!r}")
    return name


def joined(expr: str, dialect: str) -> str:
    if dialect == "spark":
        return f"concat_ws(' | ', collect_list({expr}))"
    if dialect == "mysql":
        return f"GROUP_CONCAT({expr} ORDER BY {expr} SEPARATOR ' | ')"
    return f"string_agg({expr}, ' | ' ORDER BY {expr})"


def profile_block(table: str, fields: list[str], a) -> str:
    as_text = lambda c: f"CAST({c} AS {TEXT_TYPE[a.dialect]})"
    where = ""
    if a.date_column:
        where = f" WHERE {q(a.date_column)} >= '{a.start}' AND {q(a.date_column)} < '{a.end}'"
    stats = "\n  UNION ALL\n".join(
        f"  SELECT '{f}' AS field, COUNT(*) AS n_rows,\n"
        f"         COUNT(CASE WHEN {f} IS NOT NULL AND {as_text(f)} <> '' THEN 1 END) AS n_filled,\n"
        f"         COUNT(DISTINCT {f}) AS n_distinct\n  FROM win"
        for f in fields)
    values = "\n    UNION ALL\n".join(
        f"    SELECT DISTINCT '{f}' AS field, SUBSTRING({as_text(f)}, 1, {a.width}) AS val\n"
        f"    FROM win WHERE {f} IS NOT NULL"
        for f in fields)
    return (
        f"WITH win AS (\n  SELECT {', '.join(fields)} FROM {table}{where}\n),\n"
        f"stats AS (\n{stats}\n),\n"
        f"ranked AS (\n  SELECT field, val, ROW_NUMBER() OVER (PARTITION BY field ORDER BY val) AS rn\n"
        f"  FROM (\n{values}\n  ) v\n)\n"
        f"SELECT s.field, s.n_rows, s.n_filled, s.n_distinct, {joined('r.val', a.dialect)} AS examples\n"
        f"FROM stats s\nLEFT JOIN ranked r ON r.field = s.field AND r.rn <= {a.examples}\n"
        f"GROUP BY s.field, s.n_rows, s.n_filled, s.n_distinct\nORDER BY s.field;"
    )


def profile(a) -> str:
    if a.date_column and not (a.start and a.end):
        raise SystemExit("ERROR: --start and --end are required with --date-column")
    source = a.columns.split(",") if a.columns else open(a.columns_file, encoding="utf-8").read().split()
    names = [c.strip() for c in source if c.strip()]
    personal = re.compile(a.pii_pattern, re.IGNORECASE)
    kept = [q(c) for c in names if a.keep_pii or not personal.search(c)]
    skipped = [c for c in names if c not in kept]
    parts = []
    if skipped:
        parts.append("-- left out as personal data (count them, never sample): " + ", ".join(skipped))
    for i in range(0, len(kept), a.block):
        parts.append(profile_block(q(a.table), kept[i:i + a.block], a))
    return "\n\n".join(parts)


def key_test(a) -> str:
    lt, lk, rt, rk = q(a.left), q(a.left_key), q(a.right), q(a.right_key)
    return (
        f"-- link {lt}.{lk} <-> {rt}.{rk}\n"
        f"WITH lkeys AS (SELECT {lk} AS k, COUNT(*) AS n FROM {lt} WHERE {lk} IS NOT NULL GROUP BY {lk}),\n"
        f"rkeys AS (SELECT {rk} AS k, COUNT(*) AS n FROM {rt} WHERE {rk} IS NOT NULL GROUP BY {rk})\n"
        f"SELECT\n"
        f"  (SELECT COUNT(*) FROM {lt} WHERE {lk} IS NULL) AS left_null_keys,\n"
        f"  (SELECT COUNT(*) FROM lkeys) AS left_keys,\n"
        f"  (SELECT COUNT(*) FROM lkeys WHERE n > 1) AS left_repeated_keys,\n"
        f"  (SELECT COUNT(*) FROM lkeys l WHERE NOT EXISTS (SELECT 1 FROM rkeys r WHERE r.k = l.k)) AS left_without_match,\n"
        f"  (SELECT COUNT(*) FROM {rt} WHERE {rk} IS NULL) AS right_null_keys,\n"
        f"  (SELECT COUNT(*) FROM rkeys) AS right_keys,\n"
        f"  (SELECT COUNT(*) FROM rkeys WHERE n > 1) AS right_repeated_keys,\n"
        f"  (SELECT COUNT(*) FROM rkeys r WHERE NOT EXISTS (SELECT 1 FROM lkeys l WHERE l.k = r.k)) AS right_without_match;"
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("profile")
    p.add_argument("--table", required=True)
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--columns")
    src.add_argument("--columns-file")
    p.add_argument("--dialect", default="duckdb", choices=sorted(TEXT_TYPE))
    p.add_argument("--date-column")
    p.add_argument("--start")
    p.add_argument("--end")
    p.add_argument("--block", type=int, default=10)
    p.add_argument("--examples", type=int, default=3)
    p.add_argument("--width", type=int, default=40)
    p.add_argument("--pii-pattern", default=PERSONAL)
    p.add_argument("--keep-pii", action="store_true", help="only with explicit approval")
    k = sub.add_parser("key-test")
    for flag in ("--left", "--left-key", "--right", "--right-key"):
        k.add_argument(flag, required=True)
    a = ap.parse_args(argv)
    print(profile(a) if a.cmd == "profile" else key_test(a))
    return 0


if __name__ == "__main__":
    sys.exit(main())
