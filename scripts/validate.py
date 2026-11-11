#!/usr/bin/env python3
"""Check the skill marketplace.

Structural checks live in SKILL_CHECKS and REPO_CHECKS. To add another check
later, drop a module next to this file instead of editing it:

- scripts/skill_checks/<name>.py defines check(skill, errors)
- scripts/repo_checks/<name>.py defines check(root, skills, errors)

Append strings to errors. A denylist hit must name the file only, never the term.

The leak scan reads the LEAK_DENYLIST environment variable (one term per line).
When the variable is missing or blank, the scan prints a notice and continues.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

MAX_DESCRIPTION_CHARS = 300
MAX_SKILL_LINES = 100
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ROUTE_PATH = re.compile(r"references/[A-Za-z0-9._-]+")
SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", "__pycache__"}
DENYLIST_MAX_BYTES = 5_000_000


@dataclass
class Skill:
    root: Path
    plugin: str
    directory: Path
    text: str | None
    frontmatter: dict = field(default_factory=dict)
    frontmatter_error: str | None = None

    @property
    def name(self) -> str:
        return self.directory.name

    @property
    def rel(self) -> str:
        return self.directory.relative_to(self.root).as_posix()


def parse_frontmatter(text: str) -> tuple[dict | None, str | None]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "frontmatter is missing"
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return None, "frontmatter is not closed"
    data: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            return None, "frontmatter has a line without a key"
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        if not key:
            return None, "frontmatter has an empty key"
        data[key] = value
    return data, None


def discover_skills(root: Path) -> list[Skill]:
    plugins = root / "plugins"
    skills: list[Skill] = []
    if not plugins.is_dir():
        return skills
    for plugin in sorted(path for path in plugins.iterdir() if path.is_dir()):
        skills_dir = plugin / "skills"
        if not skills_dir.is_dir():
            continue
        for directory in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
            skill_file = directory / "SKILL.md"
            text = None
            frontmatter: dict = {}
            error = None
            if skill_file.is_file():
                text = skill_file.read_text(encoding="utf-8")
                parsed, error = parse_frontmatter(text)
                frontmatter = parsed or {}
            else:
                error = "SKILL.md is missing"
            skills.append(
                Skill(
                    root=root,
                    plugin=plugin.name,
                    directory=directory,
                    text=text,
                    frontmatter=frontmatter,
                    frontmatter_error=error,
                )
            )
    return skills


def load_extra_checks(directory: Path, errors: list[str]) -> list:
    if not directory.is_dir():
        return []
    loaded = []
    for path in sorted(directory.glob("*.py")):
        if path.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(
            f"skills_check_{directory.name}_{path.stem}", path
        )
        if spec is None or spec.loader is None:
            errors.append(f"{path.name}: cannot load check module")
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as exc:  # a broken extension should fail the run, not hide
            errors.append(f"{path.as_posix()}: failed to import ({exc.__class__.__name__})")
            continue
        check = getattr(module, "check", None)
        if not callable(check):
            errors.append(f"{path.as_posix()}: must define check(...)")
            continue
        loaded.append(check)
    return loaded


def check_frontmatter(skill: Skill, errors: list[str]) -> None:
    if skill.frontmatter_error:
        errors.append(f"{skill.rel}: {skill.frontmatter_error}")
        return
    if not str(skill.frontmatter.get("name", "")).strip():
        errors.append(f"{skill.rel}: frontmatter name is missing")
    if not str(skill.frontmatter.get("description", "")).strip():
        errors.append(f"{skill.rel}: frontmatter description is missing")


def check_name_matches_folder(skill: Skill, errors: list[str]) -> None:
    if not KEBAB.fullmatch(skill.name):
        errors.append(f"{skill.rel}: folder name must be kebab-case")
    declared = skill.frontmatter.get("name")
    if declared is not None and declared != skill.name:
        errors.append(f"{skill.rel}: frontmatter name {declared!r} does not match the folder")


def check_description_length(skill: Skill, errors: list[str]) -> None:
    description = skill.frontmatter.get("description")
    if description is None:
        return
    if len(description) > MAX_DESCRIPTION_CHARS:
        errors.append(
            f"{skill.rel}: description is {len(description)} characters "
            f"(maximum {MAX_DESCRIPTION_CHARS})"
        )


def check_skill_line_count(skill: Skill, errors: list[str]) -> None:
    if skill.text is None:
        return
    count = len(skill.text.splitlines())
    if count > MAX_SKILL_LINES:
        errors.append(f"{skill.rel}: SKILL.md is {count} lines (maximum {MAX_SKILL_LINES})")


def routes_section_lines(text: str) -> list[str]:
    collected: list[str] = []
    in_section = False
    level = 0
    for line in text.splitlines():
        heading = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if heading:
            this_level = len(heading.group(1))
            title = heading.group(2).strip().lower().rstrip(":")
            if in_section and this_level <= level:
                in_section = False
            if title == "routes":
                in_section = True
                level = this_level
            continue
        if in_section:
            collected.append(line)
    return collected


def check_routes(skill: Skill, errors: list[str]) -> None:
    if skill.text is None:
        return
    section = routes_section_lines(skill.text)
    routed: list[str] = []
    for line in section:
        for token in re.findall(r"`([^`]+)`", line):
            if token.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:[\\/]", token):
                errors.append(f"{skill.rel}: route uses an absolute path")
            if ".." in token.split("/"):
                errors.append(f"{skill.rel}: route must stay inside the skill")
        routed.extend(ROUTE_PATH.findall(line))

    ref_dir = skill.directory / "references"
    if ref_dir.exists() and not ref_dir.is_dir():
        errors.append(f"{skill.rel}: references must be a directory")
        return

    present: list[str] = []
    if ref_dir.is_dir():
        for child in sorted(ref_dir.iterdir()):
            relative = f"references/{child.name}"
            if child.is_dir():
                errors.append(f"{skill.rel}: references/ must be one level deep ({relative}/)")
                continue
            if child.is_file():
                present.append(relative)

    if present and not section:
        errors.append(f"{skill.rel}: references/ exist but there is no Routes section")

    for route in routed:
        target = skill.directory / route
        if not target.is_file():
            errors.append(f"{skill.rel}: routed path does not exist ({route})")
    for relative in present:
        if relative not in routed:
            errors.append(f"{skill.rel}: {relative} is not listed in the routes table")


def check_unique_names(root: Path, skills: list[Skill], errors: list[str]) -> None:
    del root
    seen: dict[str, str] = {}
    for skill in skills:
        declared = skill.frontmatter.get("name") or skill.name
        if declared in seen:
            errors.append(
                f"skill name {declared} is used by {seen[declared]} and {skill.rel}"
            )
        else:
            seen[declared] = skill.rel


def check_skill_files_live_in_plugins(root: Path, skills: list[Skill], errors: list[str]) -> None:
    expected = {skill.directory / "SKILL.md" for skill in skills}
    for path in root.rglob("SKILL.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path not in expected:
            errors.append(
                "SKILL.md is outside plugins/<plugin>/skills/<skill>/: "
                + path.relative_to(root).as_posix()
            )


def check_marketplace_lists_plugins(root: Path, skills: list[Skill], errors: list[str]) -> None:
    del skills
    manifest_path = root / ".claude-plugin" / "marketplace.json"
    if not manifest_path.is_file():
        errors.append(".claude-plugin/marketplace.json is missing")
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        errors.append(".claude-plugin/marketplace.json is not valid JSON")
        return
    if not isinstance(manifest, dict):
        errors.append(".claude-plugin/marketplace.json must be a JSON object")
        return
    for key in ("name", "owner", "plugins"):
        if key not in manifest:
            errors.append(f"marketplace.json is missing {key}")
    owner = manifest.get("owner")
    if not isinstance(owner, dict) or not str(owner.get("name", "")).strip():
        errors.append("marketplace.json owner.name is required")
    entries = manifest.get("plugins")
    if not isinstance(entries, list):
        errors.append("marketplace.json plugins must be a list")
        return

    listed: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("marketplace.json has a plugin entry that is not an object")
            continue
        name = entry.get("name")
        source = entry.get("source")
        if not isinstance(name, str) or not name:
            errors.append("marketplace.json has a plugin entry without a name")
            continue
        if name in listed:
            errors.append(f"marketplace.json lists {name} more than once")
        expected = f"./plugins/{name}"
        if source != expected:
            errors.append(f"marketplace.json entry {name} must use source {expected}")
        plugin_dir = root / "plugins" / name
        if not plugin_dir.is_dir():
            errors.append(f"marketplace.json lists {name} but plugins/{name} does not exist")
        listed[name] = expected

    plugins_dir = root / "plugins"
    if not plugins_dir.is_dir():
        errors.append("plugins/ is missing")
        return
    for plugin in sorted(path for path in plugins_dir.iterdir() if path.is_dir()):
        if plugin.name not in listed:
            errors.append(f"plugins/{plugin.name} is not listed in marketplace.json")


def check_plugin_manifest_names(root: Path, skills: list[Skill], errors: list[str]) -> None:
    del skills
    plugins_dir = root / "plugins"
    if not plugins_dir.is_dir():
        return
    for plugin in sorted(path for path in plugins_dir.iterdir() if path.is_dir()):
        manifest_path = plugin / ".claude-plugin" / "plugin.json"
        if not manifest_path.is_file():
            continue
        relative = manifest_path.relative_to(root).as_posix()
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            errors.append(f"{relative}: invalid JSON")
            continue
        if not isinstance(manifest, dict) or manifest.get("name") != plugin.name:
            errors.append(f"{relative}: name must equal the plugin directory ({plugin.name})")


SKILL_CHECKS = [
    check_frontmatter,
    check_name_matches_folder,
    check_description_length,
    check_skill_line_count,
    check_routes,
]

REPO_CHECKS = [
    check_unique_names,
    check_skill_files_live_in_plugins,
    check_marketplace_lists_plugins,
    check_plugin_manifest_names,
]


def iter_scan_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if not path.is_file() or path.is_symlink():
            continue
        files.append(path)
    return files


def check_denylist(root: Path, errors: list[str]) -> None:
    raw = os.environ.get("LEAK_DENYLIST")
    if raw is None or not raw.strip():
        print("notice: LEAK_DENYLIST is not set; skipping the denylist scan.")
        return
    terms = [line.strip().casefold() for line in raw.splitlines() if line.strip()]
    if not terms:
        print("notice: LEAK_DENYLIST is not set; skipping the denylist scan.")
        return
    for path in iter_scan_files(root):
        relative = path.relative_to(root).as_posix()
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size > DENYLIST_MAX_BYTES:
            errors.append(f"denylist scan skipped a file over the size cap: {relative}")
            continue
        try:
            payload = path.read_bytes()
        except OSError:
            continue
        if b"\0" in payload:
            continue
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError:
            continue
        folded = text.casefold()
        if any(term in folded for term in terms):
            errors.append(f"denylist match in {relative}")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skills = discover_skills(root)
    script_dir = Path(__file__).resolve().parent
    skill_checks = SKILL_CHECKS + load_extra_checks(script_dir / "skill_checks", errors)
    repo_checks = REPO_CHECKS + load_extra_checks(script_dir / "repo_checks", errors)
    for skill in skills:
        for check in skill_checks:
            try:
                check(skill, errors)
            except Exception as exc:
                errors.append(f"{skill.rel}: check {check.__name__} failed ({exc.__class__.__name__})")
    for check in repo_checks:
        try:
            check(root, skills, errors)
        except Exception as exc:
            errors.append(f"check {check.__name__} failed ({exc.__class__.__name__})")
    check_denylist(root, errors)
    return sorted(set(errors))


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        for error in errors:
            print(error)
        print(f"validate: {len(errors)} error(s)")
        return 1
    print("validate: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
