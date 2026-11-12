"""Check knowledge/: index vs files, article size budget, history links.

  python check_knowledge.py [--root .] [--target 10000] [--max 15000]

ERROR (exit 1): index entry without file, article file missing from the index,
                duplicate id, history file not linked from any article.
WARN          : article above --target characters; SPLIT when above --max.
The size defaults are placeholders; agree them per project.
Requires PyYAML.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--target", type=int, default=10000)
    ap.add_argument("--max", type=int, default=15000)
    a = ap.parse_args(argv)
    kb = a.root / "knowledge"
    index = yaml.safe_load((kb / "index.yaml").read_text(encoding="utf-8")) or {}
    entries = index.get("articles", [])
    errors, seen, indexed = [], set(), set()
    for e in entries:
        if e.get("id") in seen:
            errors.append(f"duplicate id {e.get('id')}")
        seen.add(e.get("id"))
        f = kb / str(e.get("file"))
        indexed.add(f.resolve())
        if not f.is_file():
            errors.append(f"{e.get('id')}: file {e.get('file')} not found")
    files = [p for p in kb.rglob("*.md") if p.parent != kb and p.parent.name != "metrics"]
    for p in files:
        if p.resolve() not in indexed:
            errors.append(f"{p.relative_to(kb)} is not in index.yaml")
    texts = {p: p.read_text(encoding="utf-8") for p in files}
    for p, text in texts.items():
        size = len(text)
        if size > a.max:
            print(f"SPLIT {p.relative_to(kb)}: {size} chars > {a.max}")
        elif size > a.target:
            print(f"WARN  {p.relative_to(kb)}: {size} chars > {a.target}")
        if p.stem.endswith("-history") and not any(p.name in t for q, t in texts.items() if q != p):
            errors.append(f"{p.relative_to(kb)} is not linked from any article")
    for line in errors:
        print(f"ERROR {line}")
    if not errors:
        print("OK knowledge index consistent")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
