# Contributing

Skills are grouped into plugins. An area maintains each plugin:

| Plugin | Area |
|---|---|
| `engineering` | Engineering |
| `data-architecture` | Data architecture |
| `data-analysis` | Data analysis |
| `common` | Shared across areas |

Each area is maintained by one of Afonso's AI agents. Afonso Rocha reviews and merges.

## Pull requests

1. Work on a branch. The area that owns the skill opens the pull request.
2. A different area reviews it.
3. Afonso Rocha merges. Do not merge your own pull request.

Keep the change inside the skills you own. `common` is the cross-domain plugin: a skill goes there when more than one area uses it, or when the index already places it there. A shared skill is still one pull request, and the other area reviews the part it owns. `architecture-decision-record`, once it exists, keeps a software reference maintained with engineering and a data reference maintained with data architecture.

## Writing

Follow [CONVENTIONS.md](CONVENTIONS.md). Run `./scripts/validate.sh` before pushing. Skill names are unique across the whole repository, not only inside one plugin.

Planned skills are listed in the root [README](README.md). Add the folder when the skill is real. An empty skill directory is not a reservation. The README is.

## Extending the validator

`scripts/validate.py` holds the structural checks. Two directories can add more without editing that file:

- `scripts/skill_checks/<name>.py` defines `check(skill, errors)`. It runs once per skill. `skill` has `plugin`, `name`, `directory`, `rel`, `text`, and `frontmatter`. Append human-readable strings to `errors`. Do not include secret values.
- `scripts/repo_checks/<name>.py` defines `check(root, skills, errors)`. It runs once per repository.

The file name does not matter. The function name does. A module that fails to import fails the run.

## Versions

Releases are annotated git tags `vX.Y.Z` (semantic version). A project pins a version in either of these ways:

- Claude Code: `/plugin marketplace add afonsoalrocha/skills#vX.Y.Z`
- Any other tool: check out that tag and run `scripts/sync.sh`

Claude Code also reads `version` inside `plugin.json` and keeps an installed plugin on that version until the field changes. A release therefore does both: bump `version` in the plugin manifest, and tag the merged commit with the same number. Every plugin has a `plugin.json`, and that file is where `version` lives. Do not copy `version` onto the marketplace entry as well. When both are set, the manifest wins and `claude plugin validate` warns.

The human maintainer creates the tag after the merge. A pull request does not tag.

`scripts/sync.sh` records the commit SHA in the destination lock file. When the checkout is exactly a tag, it records that tag too.
