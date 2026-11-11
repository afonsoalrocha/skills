"""Classify the change between two contract YAML files as none, additive or breaking.

Usage: python contract_diff.py old.yaml new.yaml   (exit 2 if breaking without a version bump)
Requires PyYAML, which is not in the Python standard library.
"""

from __future__ import annotations

import sys

import yaml


def load(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def classify(old: dict, new: dict) -> tuple[str, list[str]]:
    notes: list[str] = []
    breaking = False
    oc = {c["name"]: c for c in old.get("columns", [])}
    nc = {c["name"]: c for c in new.get("columns", [])}
    for name in oc.keys() - nc.keys():
        breaking = True; notes.append(f"removed column {name}")
    for name in nc.keys() - oc.keys():
        if nc[name].get("nullable", True):
            notes.append(f"added nullable column {name}")
        else:
            breaking = True; notes.append(f"added non-nullable column {name}")
    for name in oc.keys() & nc.keys():
        a, b = oc[name], nc[name]
        if a.get("type") != b.get("type"):
            breaking = True; notes.append(f"type of {name}: {a.get('type')} -> {b.get('type')}")
        if a.get("nullable", True) is False and b.get("nullable", True) is True:
            breaking = True; notes.append(f"{name} became nullable")
        if set(b.get("accepted_values", [])) < set(a.get("accepted_values", [])):
            breaking = True; notes.append(f"{name} lost accepted values")
        if a.get("description") != b.get("description"):
            notes.append(f"description of {name} changed: confirm meaning did not change")
    for key in ("grain", "primary_key"):
        if old.get(key) != new.get(key):
            breaking = True; notes.append(f"{key} changed")
    if breaking:
        return "breaking", notes
    return ("additive" if notes else "none"), notes


def main() -> int:
    old, new = load(sys.argv[1]), load(sys.argv[2])
    kind, notes = classify(old, new)
    for n in notes:
        print(f"NOTE: {n}")
    bumped = new.get("version", 0) > old.get("version", 0)
    print(f"{'ERROR' if kind == 'breaking' and not bumped else 'OK'}: change is {kind}"
          + ("" if kind != "breaking" else f", version bumped: {bumped}"))
    return 2 if kind == "breaking" and not bumped else 0


if __name__ == "__main__":
    sys.exit(main())
