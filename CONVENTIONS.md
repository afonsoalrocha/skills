# Conventions

How skills in this repository are written. Nothing here is specific to one project. Project context lives in that project's `AGENTS.md` or `CLAUDE.md`, which points at these skills.

## Where an instruction lives

Stop at the first match.

1. It has to hold before any file is opened: a global action, creating a folder, a decision for the whole session. Put it in the project's always-on instructions (`AGENTS.md`, `CLAUDE.md`, or a rule with no path filter). Keep that layer short. A `CLAUDE.md` of about 200 lines is already long, because it loads every session.
2. It holds only while reading or editing an existing part of the tree. Put it in a path-scoped rule. The rule loads in full when it matches, so keep it short.
3. It is a procedure with steps, examples, or tables. Make it a skill.
4. A machine can enforce it. Make it a hook, a script, or a validator.
5. It is a personal preference or durable knowledge. Put it in agent memory. Do not put it in a skill.

Each rule lives in one place. When the text already exists, point to it. Do not copy it.

## Skills

One skill has one goal, and the skill is only as large as that goal. A new skill needs a trigger of its own. Two skills that always load together are one skill.

A skill is a directory at `plugins/<plugin>/skills/<skill>/`. The folder name is the skill name: kebab-case, unique across the whole repository, and equal to the frontmatter `name`.

### SKILL.md

`SKILL.md` is a short router.

Frontmatter:

- `name` is the folder name.
- `description` is the trigger, not a summary of the body. It says what someone is doing when this skill should load. Keep it to 300 characters. It is considered on every session, so length costs even when the skill does not run.

The body stays within about 100 lines:

- the objective
- the invariant rules (a rule that causes a wrong result when forgotten belongs here, not in a reference)
- a routes table: if X, read `references/x.md`

### references/

One directory, one level deep. No nested folders. Every file in `references/` has a row in the routes table, and every path in that table exists. Open a reference only when a route says to. Paths are relative to the skill and look like `references/x.md`. Do not use absolute paths.

### scripts/

A deterministic procedure (a parser, a finite check, a transform) is a program in that skill's `scripts/` directory, not a block of prose.

The `scripts/` directory at the repository root is marketplace tooling (`sync.sh`, `validate.py`). It is not a skill.

### What does not go in a skill

- A permanent preference, or knowledge that should outlive the task. That belongs in agent memory or in the project's own instructions.
- A second copy of text that already lives in another skill, a document, or the code. Point to it.
- Names, schemas, customer data, or rules from one project. See [SECURITY.md](SECURITY.md).

## Changing a skill

Decide where the new content goes before writing it. Stop at the first match.

1. A skill with the same goal already exists. Add to that skill.
2. The rule is invariant on every run of the skill. One line in the body of `SKILL.md`.
3. It matters on only one route: one case, one tool, one example, one long table. Add `references/<route>.md` and a row in the routes table. Without the row, the file will not be opened.
4. The trigger changed, because a new situation should load the skill. Only then edit `description`, and keep it short.
5. The content already exists somewhere else. Point to it.

Then run `./scripts/validate.sh`. To add a further check, see [CONTRIBUTING.md](CONTRIBUTING.md).
