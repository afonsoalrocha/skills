[![validate](https://github.com/afonsoalrocha/skills/actions/workflows/validate.yml/badge.svg)](https://github.com/afonsoalrocha/skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code plugin marketplace](https://img.shields.io/badge/Claude_Code-plugin_marketplace-181717)](https://code.claude.com/docs/en/plugins/create-marketplace)

# skills

AI coding and data agents need small, single-purpose instructions they can reuse, and they need to load only the part the current task asks for. A long guide that sits in context the whole time gets skipped, or it crowds out the work. This repository is a marketplace of those instructions. Each skill is a short router: the objective and the rules that always apply, plus a table of routes. The longer material stays in a reference file until a route says to open it.

The skills are generic. Anything that belongs to one project stays in that project's `AGENTS.md` or `CLAUDE.md`, which points here.

## Install and use

### Claude Code

In a Claude Code session, add the marketplace:

```text
/plugin marketplace add afonsoalrocha/skills
```

The marketplace name is `afonsoalrocha-skills`. Install the plugin you need:

```text
/plugin install engineering@afonsoalrocha-skills
```

The same install command accepts `data-analysis`, `common`, and `data-architecture`. `engineering`, `data-analysis`, `common`, and `data-architecture` all have skills.

To pin a release, add the marketplace at a tag. See [CONTRIBUTING.md](CONTRIBUTING.md).

```text
/plugin marketplace add afonsoalrocha/skills#vX.Y.Z
```

### Other tools

Tools that read a skills directory, instead of a plugin marketplace, can copy one plugin:

```bash
scripts/sync.sh engineering .claude/skills
scripts/sync.sh engineering .cursor/skills
```

Run the script from a clone of this repository. The first argument is the plugin name. The second is the destination skills folder. The script copies that plugin's skills and writes `<destination>/.skills-lock.json` with the source repository, the commit SHA, and the git tag when the clone is checked out exactly at a tag.

## Requirements

Skill scripts use the Python standard library, except three that need [PyYAML](https://pyyaml.org/):

- `plugins/common/skills/new-request/scripts/registry.py`
- `plugins/data-analysis/skills/knowledge-base/scripts/check_knowledge.py`
- `plugins/data-analysis/skills/bi-assets-as-code/scripts/validate_assets.py`

`close-request` calls `registry.py`, so the `common` skills install together.

## Index

One row per skill. A row marked Planned is a reserved name. The folder is not in the tree yet.

| Skill | Plugin | Owner | Purpose |
|---|---|---|---|
| `spec-next-slice` | engineering | Engineering | Decide the next slice and get its acceptance tests approved before any code. |
| `design-architecture` | engineering | Engineering | Choose a simple, testable, reversible structure for what that slice needs. |
| `implement-slice` | engineering | Engineering | Make the slice's acceptance tests pass with small, proven steps. |
| `refactor-slice` | engineering | Engineering | Tidy the structure after the slice works, without changing behavior. |
| `review-delivery` | engineering | Engineering | Prove the slice and report it in language the system owner can sign. |
| `ship-to-production` | engineering | Engineering | Ship in small reversible steps and see what production is doing. |
| `new-request` | common | Data analysis | Open, spec, register, and move a formal numbered request (analytics or engineering) in `requests/registry.yaml`. |
| `close-request` | common | Data analysis | Close a request only with explicit human approval: gates, outcome complete/partial/blocked, insight log, knowledge review, and the closed transition. |
| `session-handoff` | common | Shared | Save or resume session state in a HANDOFF.md that another session or agent can continue from. |
| `session-retrospective` | common | Shared | Review agent sessions from a collected summary and propose small, deterministic fixes. |
| `share-web-links` | common | Shared | Give stakeholders a web link computed by a script, never a disk path. |
| `stakeholder-deliverables` | common | Shared | Produce PDFs and decks from approved templates and validated data, and review every page. |
| `meeting-minutes` | common | Shared | Turn a transcript into minutes: parse it, summarize it, show the text first, then render. |
| `architecture-decision-record` | common | Shared | Planned. A software reference is maintained with engineering, and a data reference with data architecture. |
| `quick-check` | data-analysis | Data analysis | One-off check in `quick-checks/YYYY-MM-DD-slug/`, with a minimum integrity pass, auto-close the next day, and promotion to a request. |
| `metric-card` | data-analysis | Data analysis | Own a metric's meaning and status (certified/indicative/blocked), maturity, reconciliation, dated history, and definition changes. |
| `dashboard-validation` | data-analysis | Data analysis | Reproduce each dashboard number by query, walk down the layers to the source of truth, and log divergences and root cause. |
| `explore-unknown-source` | data-analysis | Data analysis | Back every claim about an unfamiliar source (links, missing fields, grain) with value profiles and a two-sided link test. |
| `knowledge-base` | data-analysis | Data analysis | Keep durable knowledge in `knowledge/` and `index.yaml`: where it goes, an agent-ready article standard, and history kept apart. |
| `aws-quicksight` | data-analysis | Data analysis | Inspect, export, edit, and test QuickSight assets with CLI v2 or boto3; read-only by default; account, profile, and region from environment variables. |
| `bi-assets-as-code` | data-analysis | Data analysis | Version published BI assets under `products/` with a manifest, changelog, unique ids, inverse relationships, and validation in proportion to the change. |
| `data-integrity-tdd` | data-architecture | Data architecture | Write the data validator first, and conclude only when it passes. |
| `sql-performance` | data-architecture | Data architecture | Read less data: project, filter, inspect the plan, and page by key. |
| `production-db-readonly` | data-architecture | Data architecture | Query production MySQL or PostgreSQL read-only, in that database's dialect. |
| `databricks-workspace` | data-architecture | Data architecture | Query Databricks and move workspace files with the CLI or a SQL client. |
| `athena-queries` | data-architecture | Data architecture | Query Athena or Trino with metadata, a byte budget, and safe result reads. |
| `recurring-pipelines` | data-architecture | Data architecture | Create or operate a recurring data job that repeats safely. |
| `python-data-scripts` | data-architecture | Data architecture | Write Python data scripts with typed identifiers, time zones, and atomic output. |
| `dbt-layered-modeling` | data-architecture | Data architecture | Place each dbt model in a layer, with a name, a key, and a materialization. |
| `data-quality-gates` | data-architecture | Data architecture | Choose quality checks, and decide which ones block publication. |
| `data-contracts` | data-architecture | Data architecture | Agree and enforce the schema, grain, freshness, and meaning of a shared dataset. |
| `leak-gate` | data-architecture | Data architecture | Block publication when a private term or a secret is present. |

Owners are areas. Each area is maintained by one of Afonso's AI agents.

## Maintainer

Maintained by [Afonso Rocha](https://www.linkedin.com/in/afonsoalrocha/).

See also [analytics-hub-template](https://github.com/afonsoalrocha/analytics-hub-template).

Licensed under the [MIT License](LICENSE). Copyright (c) 2026 Afonso Rocha.

Skill shape: [CONVENTIONS.md](CONVENTIONS.md). What stays out of this public tree: [SECURITY.md](SECURITY.md). How to add a skill: [CONTRIBUTING.md](CONTRIBUTING.md).
