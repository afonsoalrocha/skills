"""Create, list, reopen and close quick checks under quick-checks/.

  new SLUG            create quick-checks/<today>-SLUG/ with README.md and scripts/
  list                print open checks
  reopen FOLDER       set Status back to open
  close FOLDER        mark one check closed today
  close-stale         close checks from earlier days, unless they have a
                      "Keep open:" line or a HANDOFF.md (those are only reported)

Standard library only. Run from the project root (or pass --root).
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

BASE = Path("quick-checks")
STATUS_RE = re.compile(r"^- \*\*Status:\*\* .*$", re.MULTILINE)
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FOLDER_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-")

TEMPLATE = """# {day} — {title}

- **Status:** open
- **Asked by:** 
- **Related request:** none

## Question

## Sources

## How to run

## Integrity
- Grain unique:
- Row count vs source:
- Period and time zone:

## Result

## Conclusion
"""


def readme(folder: Path) -> Path:
    return folder / "README.md"


def status(folder: Path) -> str:
    m = STATUS_RE.search(readme(folder).read_text(encoding="utf-8"))
    return m.group(0).split(":**", 1)[1].strip() if m else "open"


def set_status(folder: Path, value: str) -> None:
    path = readme(folder)
    text = path.read_text(encoding="utf-8")
    line = f"- **Status:** {value}"
    text = STATUS_RE.sub(line, text, count=1) if STATUS_RE.search(text) else f"{line}\n\n{text}"
    path.write_text(text, encoding="utf-8")


def checks(root: Path) -> list[Path]:
    base = root / BASE
    return sorted(p for p in base.iterdir() if p.is_dir() and readme(p).is_file()) if base.is_dir() else []


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=Path.cwd())
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("new").add_argument("slug")
    sub.add_parser("list")
    sub.add_parser("reopen").add_argument("folder")
    sub.add_parser("close").add_argument("folder")
    sub.add_parser("close-stale")
    a = ap.parse_args(argv)
    today = date.today().isoformat()

    if a.cmd == "new":
        if not SLUG_RE.match(a.slug):
            print("ERROR: slug must be kebab-case ascii")
            return 1
        folder = a.root / BASE / f"{today}-{a.slug}"
        if folder.exists():
            print(f"ERROR: {folder} already exists")
            return 1
        (folder / "scripts").mkdir(parents=True)
        readme(folder).write_text(TEMPLATE.format(day=today, title=a.slug.replace("-", " ")), encoding="utf-8")
        print(f"OK created {folder.relative_to(a.root)}")
        return 0

    if a.cmd == "list":
        for f in checks(a.root):
            if status(f) == "open":
                print(f.name)
        return 0

    if a.cmd in ("reopen", "close"):
        folder = a.root / BASE / a.folder
        if not readme(folder).is_file():
            print(f"ERROR: {folder}/README.md not found")
            return 1
        set_status(folder, "open" if a.cmd == "reopen" else f"closed ({today})")
        print(f"OK {a.folder} {a.cmd}")
        return 0

    # close-stale
    for f in checks(a.root):
        m = FOLDER_RE.match(f.name)
        if not m or m.group(1) >= today or status(f) != "open":
            continue
        text = readme(f).read_text(encoding="utf-8")
        if "- **Keep open:**" in text:
            print(f"KEEP {f.name} (keep-open line)")
        elif (f / "HANDOFF.md").exists():
            print(f"ASK  {f.name} (has HANDOFF.md; the user decides)")
        else:
            set_status(f, f"closed ({today})")
            print(f"CLOSED {f.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
