"""A description that holds ': ' or ' #' must be quoted.

The repository parser reads frontmatter line by line, so a plain value with a colon and a
space parses here but is invalid YAML. Claude Code and other YAML readers reject the
frontmatter or drop the skill. Standard library only.
"""

from __future__ import annotations

import re

FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.S)
QUOTED_OR_BLOCK = ("\"", "'", ">", "|")


def check(skill, errors: list[str]) -> None:
    match = FRONTMATTER.match(skill.text)
    if not match:
        return
    for line in match.group(1).splitlines():
        if not line.startswith("description:"):
            continue
        value = line[len("description:"):].strip()
        if not value or value.startswith(QUOTED_OR_BLOCK):
            return
        if ": " in value or " #" in value or value.endswith(":"):
            errors.append(
                f"{skill.rel}: description contains ': ' or ' #' and is not quoted; "
                "quote it so YAML readers accept the frontmatter"
            )
        return
