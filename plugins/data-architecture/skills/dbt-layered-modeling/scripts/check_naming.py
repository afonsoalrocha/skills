"""Check dbt model file names against the layer convention.

Usage: python check_naming.py <dbt_project_dir> [--single-source]   (exit 1 on violations)
--single-source allows stg_<entity> when the project has exactly one source system.
Rules: staging -> stg_<source>__<entity> (or base_ under staging/*/base),
intermediate -> int_*, audit -> audit_*, marts -> no stg_/int_/base_ prefix.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RULES = {
    "staging": re.compile(r"^(stg_[a-z0-9]+__[a-z0-9_]+|base_[a-z0-9]+__[a-z0-9_]+)$"),
    "intermediate": re.compile(r"^int_[a-z0-9_]+$"),
    "audit": re.compile(r"^audit_[a-z0-9_]+$"),
}
MART_FORBIDDEN = re.compile(r"^(stg_|int_|base_)")


def layer_of(path: Path, models: Path) -> str:
    parts = path.relative_to(models).parts
    return parts[0] if len(parts) > 1 else ""


SINGLE_SOURCE_STAGING = re.compile(r"^stg_[a-z0-9_]+$")


def check(project: Path, single_source: bool = False) -> list[str]:
    models = project / "models"
    rules = dict(RULES)
    if single_source:
        rules["staging"] = SINGLE_SOURCE_STAGING
    problems = []
    for sql in sorted(models.rglob("*.sql")):
        name, layer = sql.stem, layer_of(sql, models)
        if not re.fullmatch(r"[a-z0-9_]+", name):
            problems.append(f"{sql}: use lowercase snake_case")
        elif layer in rules and not rules[layer].match(name):
            problems.append(f"{sql}: does not match the {layer} pattern")
        elif layer == "marts" and MART_FORBIDDEN.match(name):
            problems.append(f"{sql}: mart carries a staging/intermediate prefix")
    return problems


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    project = Path(args[0] if args else ".")
    problems = check(project, single_source="--single-source" in sys.argv)
    for p in problems:
        print(f"ERROR: {p}")
    print("OK: naming" if not problems else f"ERROR: {len(problems)} naming problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
