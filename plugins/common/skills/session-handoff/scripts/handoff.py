"""Write, read and list HANDOFF.md files so a session can continue elsewhere.

The handoff lives in the folder of the work it describes and is overwritten on each
save (git keeps the history). It never holds data rows or credentials: the script
refuses text that looks like a secret and files longer than MAX_LINES.

Commands:
  write FOLDER --from AGENT --goal TEXT --next TEXT [options]
  read FOLDER
  list ROOT [ROOT ...] [--limit N]    most recent handoffs under the given roots

Exit code 0 = ok, 1 = nothing found, 2 = refused or invalid input.
Standard library only; output is ASCII.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

FILE_NAME = "HANDOFF.md"
STATES = ("in_progress", "in_review", "blocked")
MAX_LINES = 80
SECRET = re.compile(
    r"AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{20,}\.|-----BEGIN [A-Z ]*PRIVATE KEY|"
    r"\b(?:ghp|gho|sk|xox[bp])[-_][A-Za-z0-9_-]{16,}|"
    r"(?i:(password|passwd|secret|token|api[_-]?key))\s*[=:]\s*\S{6,}"
)


def ascii_text(value: str) -> str:
    """Single-line ASCII version of user text, so the file and the console stay plain."""
    return " ".join(value.split()).encode("ascii", "replace").decode("ascii")


def git_line(folder: Path) -> str:
    """Branch and number of changed files in the folder, or 'git unavailable'."""
    def run(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=folder, capture_output=True, text=True, check=True
        ).stdout.strip()

    try:
        changed = len(run("status", "--short", "--", ".").splitlines())
        return f"{run('rev-parse', '--abbrev-ref', 'HEAD')}; {changed} changed file(s) in this folder"
    except (OSError, subprocess.CalledProcessError):
        return "git unavailable"


def section(title: str, items: list[str] | None) -> list[str]:
    """Render one section; an empty section stays visible as 'none'."""
    return ["", f"## {title}", *(f"- {ascii_text(i)}" for i in (items or ["none"]))]


def write(args: argparse.Namespace) -> int:
    folder = Path(args.folder)
    if not folder.is_dir():
        print(f"ERROR: folder not found: {folder}")
        return 2
    lines = [
        f"# Handoff - {folder.resolve().name}",
        "",
        f"- Updated: {datetime.now().astimezone():%Y-%m-%d %H:%M %z}",
        f"- From: {ascii_text(args.sender)}" + (f" | To: {ascii_text(args.to)}" if args.to else ""),
        f"- State: {args.state} (never 'done' without the user's explicit approval)",
        f"- Git: {git_line(folder)}",
        "",
        "## Goal",
        ascii_text(args.goal),
        *section("Done (with evidence: script, file or number)", args.done),
        *section("Decisions", args.decision),
        *section("Pending and blockers", args.pending),
        "",
        "## Next step",
        ascii_text(args.next),
        *section("Cache and outputs", args.cache),
    ]
    text = "\n".join(lines) + "\n"
    if SECRET.search(text):
        print("ERROR: text looks like a secret; remove credentials and try again")
        return 2
    if len(lines) > MAX_LINES:
        print(f"ERROR: handoff has {len(lines)} lines (max {MAX_LINES}); summarize and point to scripts")
        return 2
    target = folder / FILE_NAME
    partial = target.with_name(FILE_NAME + ".partial")
    partial.write_text(text, encoding="utf-8", newline="\n")
    os.replace(partial, target)  # atomic: readers never see half a file
    print(f"OK: {FILE_NAME} saved in {folder}")
    return 0


def read(args: argparse.Namespace) -> int:
    path = Path(args.folder) / FILE_NAME
    if not path.is_file():
        print(f"WARN: no {FILE_NAME} in {args.folder}; start from the folder README")
        return 1
    sys.stdout.write(path.read_text(encoding="utf-8").encode("ascii", "replace").decode("ascii"))
    return 0


def list_all(args: argparse.Namespace) -> int:
    found = [p for root in args.roots for p in Path(root).glob(f"**/{FILE_NAME}")]
    found.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    if not found:
        print("WARN: no handoff found under the given roots")
        return 1
    for path in found[: args.limit]:
        state = next(
            (m.group(1) for line in path.read_text(encoding="utf-8").splitlines()
             if (m := re.match(r"- State: (\w+)", line))),
            "?",
        )
        stamp = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        print(f"{stamp}  {state:<12} {path.parent.as_posix()}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("write", help="save HANDOFF.md in a work folder")
    w.add_argument("folder", help="folder of the request or quick check")
    w.add_argument("--from", dest="sender", required=True, help="agent that is leaving")
    w.add_argument("--to", help="agent that should continue (optional)")
    w.add_argument("--state", choices=STATES, default="in_progress")
    w.add_argument("--goal", required=True)
    w.add_argument("--next", required=True, help="first concrete action for whoever continues")
    for name in ("done", "decision", "pending", "cache"):
        w.add_argument(f"--{name}", action="append", help="repeatable")
    w.set_defaults(func=write)
    r = sub.add_parser("read", help="print the handoff of a folder")
    r.add_argument("folder")
    r.set_defaults(func=read)
    ls = sub.add_parser("list", help="list the most recent handoffs under the roots")
    ls.add_argument("roots", nargs="+", help="folders to search")
    ls.add_argument("--limit", type=int, default=5)
    ls.set_defaults(func=list_all)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
