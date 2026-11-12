#!/usr/bin/env python3
"""Failures the validator must catch, plus sync of the engineering plugin."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import validate  # noqa: E402


MIN_SKILL = """---
name: demo
description: "Use when exercising the validator on a tiny skill."
---

# Demo

Objective: a fixture.

## Invariant rules

- Stay tiny.

## Routes

| If | Read |
|---|---|
| the only route | `references/note.md` |
"""


def write_repo(root: Path, skill: str = MIN_SKILL, second: str | None = None) -> None:
    plugin = root / "plugins" / "engineering"
    skill_dir = plugin / "skills" / "demo"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(skill, encoding="utf-8")
    (skill_dir / "references").mkdir()
    (skill_dir / "references" / "note.md").write_text("A note.\n", encoding="utf-8")
    (plugin / ".claude-plugin").mkdir()
    (plugin / ".claude-plugin" / "plugin.json").write_text(
        json.dumps({"name": "engineering"}) + "\n", encoding="utf-8"
    )
    plugins = [{"name": "engineering", "source": "./plugins/engineering"}]
    if second is not None:
        other = root / "plugins" / "common" / "skills" / "demo"
        other.mkdir(parents=True)
        (other / "SKILL.md").write_text(second, encoding="utf-8")
        plugins.append({"name": "common", "source": "./plugins/common"})
    marketplace = {
        "name": "example",
        "owner": {"name": "Example"},
        "plugins": plugins,
    }
    manifest = root / ".claude-plugin"
    manifest.mkdir()
    (manifest / "marketplace.json").write_text(
        json.dumps(marketplace, indent=2) + "\n", encoding="utf-8"
    )


class ValidateTests(unittest.TestCase):
    def setUp(self) -> None:
        self._denylist = os.environ.pop("LEAK_DENYLIST", None)
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)

    def tearDown(self) -> None:
        self.tmpdir.cleanup()
        if self._denylist is not None:
            os.environ["LEAK_DENYLIST"] = self._denylist
        else:
            os.environ.pop("LEAK_DENYLIST", None)

    def test_repository_is_valid(self) -> None:
        errors = validate.validate(REPO)
        self.assertEqual(errors, [], "\n".join(errors))

    def test_minimal_fixture_is_valid(self) -> None:
        write_repo(self.root)
        self.assertEqual(validate.validate(self.root), [])

    def test_name_must_match_folder(self) -> None:
        write_repo(self.root, MIN_SKILL.replace("name: demo", "name: other-name"))
        errors = validate.validate(self.root)
        self.assertTrue(any("does not match the folder" in error for error in errors))

    def test_description_length(self) -> None:
        long_description = "x" * (validate.MAX_DESCRIPTION_CHARS + 1)
        skill = MIN_SKILL.replace(
            "Use when exercising the validator on a tiny skill.",
            long_description,
        )
        write_repo(self.root, skill)
        errors = validate.validate(self.root)
        self.assertTrue(any("description is" in error for error in errors))

    def test_skill_line_count(self) -> None:
        skill = MIN_SKILL + "\n".join(f"- line {index}" for index in range(120))
        write_repo(self.root, skill)
        errors = validate.validate(self.root)
        self.assertTrue(any("SKILL.md is" in error for error in errors))

    def test_missing_route_target_and_unlisted_reference(self) -> None:
        skill = MIN_SKILL.replace("references/note.md", "references/missing.md")
        write_repo(self.root, skill)
        errors = validate.validate(self.root)
        self.assertTrue(any("does not exist" in error for error in errors))
        self.assertTrue(any("note.md" in error and "not listed" in error for error in errors))

    def test_nested_reference_is_rejected(self) -> None:
        write_repo(self.root)
        nested = self.root / "plugins" / "engineering" / "skills" / "demo" / "references" / "nested"
        nested.mkdir()
        (nested / "deep.md").write_text("no\n", encoding="utf-8")
        errors = validate.validate(self.root)
        self.assertTrue(any("one level deep" in error for error in errors))

    def test_duplicate_skill_names(self) -> None:
        write_repo(self.root, second=MIN_SKILL)
        errors = validate.validate(self.root)
        self.assertTrue(any("skill name demo is used by" in error for error in errors))

    def test_marketplace_must_list_every_plugin(self) -> None:
        write_repo(self.root)
        (self.root / "plugins" / "common").mkdir()
        (self.root / "plugins" / "common" / "README.md").write_text("placeholder\n", encoding="utf-8")
        errors = validate.validate(self.root)
        self.assertTrue(any("plugins/common is not listed" in error for error in errors))

    def test_denylist_reports_the_file_and_hides_the_term(self) -> None:
        write_repo(self.root)
        marker = "zz-private-marker-zz"
        (self.root / "plugins" / "engineering" / "README.md").write_text(
            f"notes {marker} end\n", encoding="utf-8"
        )
        os.environ["LEAK_DENYLIST"] = f"\n{marker}\n"
        errors = validate.validate(self.root)
        joined = "\n".join(errors)
        self.assertIn("denylist match in plugins/engineering/README.md", joined)
        self.assertNotIn(marker, joined)

    def test_denylist_absent_is_a_notice(self) -> None:
        write_repo(self.root)
        os.environ.pop("LEAK_DENYLIST", None)
        with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as handle:
            saved = sys.stdout
            try:
                sys.stdout = handle
                errors = validate.validate(self.root)
                handle.seek(0)
                notice = handle.read()
            finally:
                sys.stdout = saved
        self.assertEqual(errors, [])
        self.assertIn("LEAK_DENYLIST is not set", notice)

    def test_extra_skill_check_is_picked_up(self) -> None:
        folder = REPO / "scripts" / "skill_checks"
        folder.mkdir(exist_ok=True)
        module = folder / "example_check.py"
        module.write_text(
            "def check(skill, errors):\n"
            "    if skill.name == 'spec-next-slice':\n"
            "        errors.append('extra-check-saw-spec-next-slice')\n",
            encoding="utf-8",
        )
        try:
            errors = validate.validate(REPO)
            self.assertIn("extra-check-saw-spec-next-slice", errors)
        finally:
            module.unlink(missing_ok=True)
            cache = folder / "__pycache__"
            if cache.exists():
                shutil.rmtree(cache)
            folder.rmdir()


class SyncTests(unittest.TestCase):
    def test_sync_copies_skills_and_records_the_commit(self) -> None:
        dest = Path(tempfile.mkdtemp())
        try:
            completed = subprocess.run(
                ["bash", "scripts/sync.sh", "engineering", str(dest)],
                cwd=REPO,
                check=True,
                text=True,
                capture_output=True,
            )
            self.assertIn("synced engineering", completed.stdout)
            self.assertTrue((dest / "spec-next-slice" / "SKILL.md").is_file())
            self.assertTrue(
                (dest / "refactor-slice" / "references" / "metrics.md").is_file()
            )
            lock = json.loads((dest / ".skills-lock.json").read_text(encoding="utf-8"))
            head = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=REPO, text=True
            ).strip()
            entry = lock["plugins"]["engineering"]
            self.assertEqual(lock["source"], "https://github.com/afonsoalrocha/skills")
            self.assertEqual(entry["commit"], head)
            self.assertIsNone(entry["tag"])
            self.assertEqual(
                entry["skills"],
                [
                    "agent-session-worktrees",
                    "azure-devops-rest-pitfalls",
                    "design-architecture",
                    "implement-slice",
                    "refactor-slice",
                    "review-delivery",
                    "ship-to-production",
                    "spec-next-slice",
                ],
            )

            stale = dest / "spec-next-slice"
            self.assertTrue(stale.is_dir())
            lock["plugins"]["engineering"]["skills"].append("retired-skill")
            (dest / "retired-skill").mkdir()
            (dest / "retired-skill" / "SKILL.md").write_text("gone\n", encoding="utf-8")
            (dest / ".skills-lock.json").write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
            subprocess.run(
                ["bash", "scripts/sync.sh", "engineering", str(dest)],
                cwd=REPO,
                check=True,
                text=True,
                capture_output=True,
            )
            self.assertFalse((dest / "retired-skill").exists())
            self.assertTrue((dest / "spec-next-slice" / "SKILL.md").is_file())
        finally:
            shutil.rmtree(dest)

    def test_sync_rejects_an_unknown_plugin(self) -> None:
        dest = Path(tempfile.mkdtemp())
        try:
            completed = subprocess.run(
                ["bash", "scripts/sync.sh", "missing", str(dest)],
                cwd=REPO,
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("unknown plugin", completed.stderr)
        finally:
            shutil.rmtree(dest)


if __name__ == "__main__":
    unittest.main()
