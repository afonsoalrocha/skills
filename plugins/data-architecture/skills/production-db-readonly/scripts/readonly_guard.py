"""Reject SQL that is not a read. Defense in depth only: grants on the DB user are the real control.

Usage: python readonly_guard.py "SELECT ..."   (exit 0 = allowed, 1 = refused)
"""

from __future__ import annotations

import re
import sys

ALLOWED_FIRST = {"select", "with", "show", "describe", "desc", "explain", "values"}
FORBIDDEN_ANYWHERE = re.compile(
    r"\b(insert|update|delete|merge|upsert|replace|create|alter|drop|truncate|grant|revoke|"
    r"call|exec|execute|copy|load|lock|vacuum|analyze|optimize|set\s+global)\b",
    re.IGNORECASE,
)


def strip_comments_and_strings(sql: str) -> str:
    sql = re.sub(r"--[^\n]*", " ", sql)
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.DOTALL)
    sql = re.sub(r"'(?:''|[^'])*'", "''", sql)
    return sql


def is_read_only(sql: str) -> tuple[bool, str]:
    clean = strip_comments_and_strings(sql).strip().rstrip(";")
    if ";" in clean:
        return False, "multiple statements"
    words = clean.split(None, 1)
    if not words:
        return False, "empty statement"
    first = words[0].lower()
    if first not in ALLOWED_FIRST:
        return False, f"first verb '{first}' is not a read"
    if first == "explain" and re.search(r"\banalyze\b", clean, re.IGNORECASE):
        return False, "EXPLAIN ANALYZE executes the statement; needs explicit approval"
    hit = FORBIDDEN_ANYWHERE.search(clean if first != "explain" else clean[len("explain"):])
    if hit:
        return False, f"forbidden keyword '{hit.group(1)}'"
    return True, "ok"


def main() -> int:
    ok, reason = is_read_only(" ".join(sys.argv[1:]))
    print(("OK: " if ok else "ERROR: ") + reason)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
