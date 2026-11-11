"""Leak gate: private denylist scan plus secret regexes over a folder.

Usage: python leak_scan.py [--denylist FILE] [--hide-terms] PATH [PATH ...]
Exit 1 on any hit. Denylist: one term per line, '#' comments; terms < 4 chars use word boundaries.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", "target"}
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".parquet", ".duckdb", ".zip", ".gz"}
FORBIDDEN_NAMES = {".env", ".leak-denylist.txt"}

SECRET_PATTERNS = {
    "aws_access_key_id": r"\b(AKIA|ASIA)[0-9A-Z]{16}\b",
    "github_token": r"\bgh[pousr]_[A-Za-z0-9]{36,}\b|\bgithub_pat_[A-Za-z0-9_]{60,}\b",
    "gitlab_token": r"\bglpat-[A-Za-z0-9_-]{20,}\b",
    "slack_token": r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b",
    "google_api_key": r"\bAIza[0-9A-Za-z_-]{35}\b",
    "databricks_token": r"\bdapi[0-9a-f]{32}\b",
    "private_key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "jwt": r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b",
    "url_credentials": r"[a-z][a-z0-9+.-]*://[^/\s:@]+:[^/\s:@<>]+@",
    "assignment": r"(?i)\b(password|passwd|secret|token|api_key|apikey)\s*[:=]\s*['\"][^'\"<>\s]{8,}['\"]",
}


def load_terms(path: Path | None) -> list[str]:
    if not path or not path.is_file():
        return []
    terms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            terms.append(line.casefold())
    return terms


def term_regex(term: str) -> re.Pattern[str]:
    escaped = re.escape(term)
    if len(term) < 4 or term.isalpha() and len(term) <= 5:
        return re.compile(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])")
    return re.compile(escaped)


def iter_files(roots: list[Path]):
    for root in roots:
        files = [root] if root.is_file() else root.rglob("*")
        for f in files:
            if f.is_file() and not (set(f.parts) & SKIP_DIRS) and f.suffix.lower() not in SKIP_SUFFIXES:
                yield f


def scan(roots: list[Path], terms: list[str], hide: bool, denylist: Path | None) -> list[str]:
    hits = []
    regs = [(t, term_regex(t)) for t in terms]
    secrets = {k: re.compile(v) for k, v in SECRET_PATTERNS.items()}
    for f in iter_files(roots):
        if denylist and f.resolve() == denylist.resolve():
            continue
        if f.name in FORBIDDEN_NAMES:
            hits.append(f"{f}: forbidden file present")
            continue
        data = f.read_bytes()
        if b"\0" in data[:1024]:
            continue
        for n, line in enumerate(data.decode("utf-8", errors="replace").splitlines(), 1):
            low = line.casefold()
            for term, rx in regs:
                if rx.search(low):
                    label = hashlib.sha256(term.encode()).hexdigest()[:8] if hide else term
                    hits.append(f"{f}:{n}: denylist term [{label}]")
            for name, rx in secrets.items():
                if rx.search(line):
                    hits.append(f"{f}:{n}: possible secret [{name}]")
    return hits


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("paths", nargs="+", type=Path)
    p.add_argument("--denylist", type=Path)
    p.add_argument("--hide-terms", action="store_true", help="print term hashes, for public CI logs")
    a = p.parse_args()
    terms = load_terms(a.denylist)
    if not terms:
        print("WARN: no denylist terms loaded; only secret patterns ran. This is NOT a clean leak scan.")
    hits = scan(a.paths, terms, a.hide_terms, a.denylist)
    for h in hits:
        print(f"ERROR: {h}")
    print(f"{'ERROR' if hits else 'OK'}: {len(hits)} hits, {len(terms)} terms")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
