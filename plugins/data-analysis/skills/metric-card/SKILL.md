---
name: metric-card
description: "Define, revise, certify, downgrade or block a business metric in its card (knowledge/metrics/<id>.yaml): definition, formula, grain, filters, maturity, reconciliation, status certified/indicative/blocked, dated history. Sole owner of metric meaning; catalog validation is data engineering."
---

# Metric card

The metric card is the **single source of a metric's meaning and status**. Requests,
quick checks, dashboards and knowledge articles link to the card; they never redefine
the metric. The project's metric-catalog validation (schema checks, CI, publishing gates,
owned by data engineering: `data-contracts`, `data-quality-gates`)
**consumes** the card; this skill decides what the card says.

## Rules that always apply

- One YAML file per metric in `knowledge/metrics/<id>.yaml`, listed in the knowledge index.
  `id` is stable and snake_case; never reuse an id for a different meaning.
- `status` is one of:
  - `certified`: definition approved by its owner, checks pass, reconciles with its source.
  - `indicative`: usable with a label; published only with the `_indicative` suffix.
  - `blocked`: cannot be answered reliably; `block_reason` is required, the metric is
    published nowhere, and the card documents the question it cannot answer and why.
- Any other status keeps `block_reason: null`.
- The human owner decides definition and status. The agent drafts and proposes.
- A definition change updates the card **in the same piece of work** that discovered it,
  not later at close. Stale definitions make the next analysis wrong.
- `history` is append-only and dated. The current rule is the card body; earlier rules
  stay in history (and in a history article when the change is large).
- Every certified answer shows period, filters, unit and the time of the last data load.

## Steps

1. Search first: `rg -i "<metric id|business name|key column>" knowledge requests products`.
   If a card exists, revise it; do not create a near-duplicate.
2. New card: copy the template in `references/card-template.md`.
3. Fill every field. Formula names numerator, denominator and aggregation explicitly.
4. Choose the status with `references/status-and-maturity.md`.
5. Append the change to `history` with date, what changed and who decided.
6. Add or update the id in the knowledge index; run the project's catalog validation.
7. If the definition changed, follow `references/definition-change.md`.

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| Card fields and the YAML template | `references/card-template.md` |
| Choosing certified / indicative / blocked, maturity window, reconciliation | `references/status-and-maturity.md` |
| Changing an existing definition, column or source without losing history | `references/definition-change.md` |

Durable knowledge that is not a metric (business context, data traps, processes):
skill `knowledge-base`.
