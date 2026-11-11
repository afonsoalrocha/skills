"""Deterministic helper for requests/registry.yaml.

Commands:
  next                                   print the next request id
  open ID SLUG TITLE [--requester R] [--owner O]
  move ID STATUS REASON                  append a lifecycle transition
  close ID OUTCOME REASON                append `closed` and set the outcome
  validate                               check the registry against the folders

Run from the project root (or pass --root). Requires PyYAML.
Exit code 0 = ok, 1 = validation or transition error.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

import yaml

REGISTRY = Path("requests") / "registry.yaml"
STATUSES = ("open", "in_spec", "in_build", "in_interpretation", "closed", "paused")
OUTCOMES = ("complete", "partial", "blocked")
ALLOWED = {
    "open": {"in_spec", "paused"},
    "in_spec": {"in_build", "paused"},
    "in_build": {"in_interpretation", "in_spec", "paused"},
    "in_interpretation": {"closed", "in_build", "paused"},
    "closed": {"in_interpretation"},
}


def _norm(value):
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {("on" if k is True else str(k)): _norm(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_norm(v) for v in value]
    return value


def load(root: Path) -> dict:
    path = root / REGISTRY
    if not path.exists():
        return {"version": 1, "requests": []}
    doc = _norm(yaml.safe_load(path.read_text(encoding="utf-8")) or {})
    doc.setdefault("requests", [])
    return doc


def save(root: Path, doc: dict) -> None:
    path = root / REGISTRY
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".yaml.part")
    tmp.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
    tmp.replace(path)  # atomic write


def find(doc: dict, request_id: str) -> dict:
    for item in doc["requests"]:
        if str(item.get("id")) == request_id:
            return item
    raise SystemExit(f"ERROR: request {request_id} not in registry")


def previous_active(item: dict) -> str | None:
    for t in reversed(item.get("transitions", [])[:-1]):
        if t.get("to") != "paused":
            return t.get("to")
    return None


def can_move(item: dict, target: str) -> bool:
    current = item.get("status")
    if target == "paused":
        return current not in ("paused", "closed")
    if current == "paused":
        return target == previous_active(item)
    return target in ALLOWED.get(current, set())


def cmd_next(root: Path, _args) -> int:
    ids = [int(str(r["id"])) for r in load(root)["requests"] if str(r.get("id", "")).isdigit()]
    print(f"{(max(ids) + 1) if ids else 1:03d}")
    return 0


def cmd_open(root: Path, args) -> int:
    doc = load(root)
    if any(str(r.get("id")) == args.id for r in doc["requests"]):
        print(f"ERROR: id {args.id} already exists")
        return 1
    today = date.today().isoformat()
    doc["requests"].append({
        "id": args.id,
        "slug": args.slug,
        "title": args.title,
        "path": f"requests/{args.id}-{args.slug}",
        "status": "open",
        "requester_role": args.requester,
        "owner": args.owner,
        "opened_on": today,
        "tags": [],
        "sources": [],
        "external_ticket": None,
        "transitions": [{"on": today, "to": "open", "reason": args.reason}],
    })
    (root / "requests" / f"{args.id}-{args.slug}").mkdir(parents=True, exist_ok=True)
    save(root, doc)
    print(f"OK opened {args.id}-{args.slug}")
    return 0


def _append(root: Path, request_id: str, target: str, reason: str, outcome: str | None) -> int:
    doc = load(root)
    item = find(doc, request_id)
    if not reason.strip():
        print("ERROR: a reason is required")
        return 1
    if not can_move(item, target):
        print(f"ERROR: {item.get('status')} -> {target} is not allowed")
        return 1
    item.setdefault("transitions", []).append(
        {"on": date.today().isoformat(), "to": target, "reason": reason}
    )
    item["status"] = target
    if target == "closed":
        item["outcome"] = outcome
    elif "outcome" in item:
        del item["outcome"]  # reopened: the outcome no longer holds
    save(root, doc)
    print(f"OK {request_id} -> {target}" + (f" ({outcome})" if outcome else ""))
    return 0


def cmd_move(root: Path, args) -> int:
    if args.status == "closed":
        print("ERROR: use `close` (close-request skill) to close a request")
        return 1
    return _append(root, args.id, args.status, args.reason, None)


def cmd_close(root: Path, args) -> int:
    if args.outcome == "blocked":
        print("ERROR: a blocked outcome does not close; the request stays open")
        return 1
    return _append(root, args.id, "closed", args.reason, args.outcome)


def cmd_validate(root: Path, _args) -> int:
    problems: list[str] = []
    seen: set[str] = set()
    for item in load(root)["requests"]:
        rid, slug = str(item.get("id")), str(item.get("slug"))
        if rid in seen:
            problems.append(f"{rid}: duplicate id")
        seen.add(rid)
        folder = f"requests/{rid}-{slug}"
        if item.get("path") != folder:
            problems.append(f"{rid}: path must be {folder}")
        if not (root / folder / "README.md").is_file():
            problems.append(f"{rid}: {folder}/README.md is missing")
        transitions = item.get("transitions") or []
        if not transitions:
            problems.append(f"{rid}: no transitions")
            continue
        last = None
        for t in transitions:
            if t.get("to") not in STATUSES:
                problems.append(f"{rid}: unknown status {t.get('to')}")
            if not str(t.get("reason", "")).strip():
                problems.append(f"{rid}: transition without reason")
            if last and str(t.get("on")) < last:
                problems.append(f"{rid}: transitions out of date order")
            last = str(t.get("on"))
        if item.get("status") != transitions[-1].get("to"):
            problems.append(f"{rid}: status differs from the last transition")
        outcome = item.get("outcome")
        if item.get("status") == "closed":
            if outcome not in ("complete", "partial"):
                problems.append(f"{rid}: closed request needs outcome complete or partial")
        elif outcome is not None:
            problems.append(f"{rid}: outcome is only allowed on a closed request")
    for line in problems:
        print(f"ERROR {line}")
    if not problems:
        print("OK registry valid")
    return 1 if problems else 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", type=Path, default=Path.cwd())
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("next")
    o = sub.add_parser("open")
    o.add_argument("id")
    o.add_argument("slug")
    o.add_argument("title")
    o.add_argument("--requester", default="unknown")
    o.add_argument("--owner", default="unknown")
    o.add_argument("--reason", default="Request accepted into the registry.")
    m = sub.add_parser("move")
    m.add_argument("id")
    m.add_argument("status", choices=[s for s in STATUSES])
    m.add_argument("reason")
    c = sub.add_parser("close")
    c.add_argument("id")
    c.add_argument("outcome", choices=OUTCOMES)
    c.add_argument("reason")
    sub.add_parser("validate")
    args = p.parse_args(argv)
    handler = {"next": cmd_next, "open": cmd_open, "move": cmd_move,
               "close": cmd_close, "validate": cmd_validate}[args.cmd]
    return handler(args.root, args)


if __name__ == "__main__":
    sys.exit(main())
