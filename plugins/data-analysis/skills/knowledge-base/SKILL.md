---
name: knowledge-base
description: Record, update, split or retire durable project knowledge in knowledge/ (business context, dashboards, data traps, sources of truth, processes) and keep knowledge/index.yaml in sync for agents and humans. Metric definitions go to metric-card; pipeline and engineering docs to data engineering.
---

# Knowledge base

`knowledge/` in git is the **canonical** knowledge of the project. Any wiki or portal is a
published mirror: changes are made in git first and published after, never the reverse.

It grows as work teaches something new. It must be fast for agents and readable for
humans: navigate from business to detail, find the right article by layer, source,
metric, dashboard or tag.

## Rules that always apply

- Read `knowledge/index.yaml` before opening many articles; update it whenever an article
  is created, moved, renamed, retired or published.
- **Same piece of work**: when work discovers or changes a rule that a reader relies on
  (a source of truth, a column meaning, a dashboard behaviour), update the article before
  that work ends, not at close. Metric definitions themselves change in `metric-card`.
- **Current summary on top**: what is valid today, the limits that change an answer, and
  what was superseded. History lives in a sub-article, never stacked as "Update of <date>".
- Old rules are moved to history, never deleted. Check that no non-empty line was lost.
- Every number is dated and sourced; counts from one load are evidence of that date, not
  constants.
- Separate validated fact, inference and open question.
- No secrets, personal data or local disk paths in articles; link outputs by shareable URL.
- Publish outside the repository only after merge to the main branch and with approval.

## Where knowledge goes (layers, highest first)

| Learning | Layer folder |
|----------|--------------|
| Product, channel, stakeholder or business decision context | `business/` |
| Metric definition, official filter, calculation rule | `metrics/` (cards, skill `metric-card`) |
| Panel, page, visual, display rule, validation result | `dashboards/` |
| Table, column, join, source of truth, data trap | `data/` |
| Pipeline, job, lineage, performance | `engineering/` (owned by data engineering) |
| Ritual, recurring task, access, ownership | `processes/` |
| Reusable tool patterns | `tools/` |

When a topic crosses layers, write a short explanation in the highest layer and link down.
Do not create separate roots per team or product line; use tags and an index field.

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| Update vs create vs split an article; the agent-ready article standard | `references/articles.md` |
| `index.yaml` fields and folder layout | `references/index-and-layout.md` |
| Checking index, sizes and history links | `python scripts/check_knowledge.py --help` (paths relative to this skill) |

Knowledge review at the end of a request: skill `close-request`.
