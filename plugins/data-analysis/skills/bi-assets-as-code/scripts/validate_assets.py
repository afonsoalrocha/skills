"""Validate products/**/asset.yaml manifests.

ERROR (exit 1): id differs from folder name, duplicate resource_id across all assets,
relationship target missing, inverse relationship missing, CHANGELOG.md missing.
Requires PyYAML.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

INVERSE = {"uses_dataset": "used_by_dashboard", "in_container": "contains", "feeds": "fed_by"}
INVERSE.update({v: k for k, v in list(INVERSE.items())})


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path.cwd())
    a = ap.parse_args(argv)
    assets, errors, resource_ids = {}, [], {}
    for path in sorted((a.root / "products").rglob("asset.yaml")):
        m = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        aid = m.get("id")
        if aid != path.parent.name:
            errors.append(f"{path}: id {aid!r} differs from folder {path.parent.name!r}")
        if not (path.parent / "CHANGELOG.md").is_file():
            errors.append(f"{aid}: CHANGELOG.md missing")
        rid = m.get("resource_id")
        if rid:
            if rid in resource_ids:
                errors.append(f"resource_id {rid} used by {resource_ids[rid]} and {aid}")
            resource_ids[rid] = aid
        assets[aid] = m
    for aid, m in assets.items():
        for rel in m.get("relationships") or []:
            target, kind = rel.get("target"), rel.get("type")
            if target not in assets:
                errors.append(f"{aid}: relationship target {target} not found")
                continue
            inverse = INVERSE.get(kind)
            back = {(r.get("type"), r.get("target")) for r in assets[target].get("relationships") or []}
            if inverse and (inverse, aid) not in back:
                errors.append(f"{aid} -{kind}-> {target}: inverse {inverse} missing in {target}")
    for e in errors:
        print(f"ERROR {e}")
    print("OK manifests consistent" if not errors else f"{len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
