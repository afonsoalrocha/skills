---
name: dashboard-validation
description: Check whether the numbers shown on a dashboard or report (any BI tool) are correct by reproducing each one with a query and walking down the layers to the source of truth, recording matches, divergences and root cause. Not for building dashboards or for pipeline data tests.
---

# Dashboard validation

Before starting, write down the chain of places each number passes through, from what
the reader sees back to where the fact was first recorded. Typically:

1. the visual and its filters;
2. the table or dataset the BI tool reads;
3. the modelled layers that feed it (one or more);
4. the operational system where the event is recorded, which is the final arbiter.

Layer names differ per project; use the project's own names in the README.

## Rules that always apply

- A dashboard visual or a BI semantic model is never the source. Reconcile against the
  data before claiming a number is right or wrong.
- Reproduce each number with a versioned query or script; never by eye or by copying a
  total from another report.
- Declare what is being compared: which published version of the dashboard, which filters,
  which data load (date and time). Comparing against an old copy creates false divergences.
- Same filters, period, time zone and grain as the visual. Write them down per number.
- Compare with an explicit tolerance (absolute or relative); never exact equality for
  currency values.
- A metric with a card is reproduced from the card's definition. If the dashboard uses a
  different definition, that is the finding.
- Access failures (permission errors, timeouts) are not "no data": retry or report them.

## Steps

1. List every number to validate: visual, filters, period, unit. One row each.
2. Identify the tables (and layer) behind each number.
3. Reproduce each number by query, starting at the serving layer.
4. Compare with `python scripts/compare_numbers.py <file.csv>` (paths relative to this
   skill). Matches are done.
5. For each divergence go one layer down, and if needed down to the source system, until
   the layer where the number first diverges is found.
6. Record per number: dashboard value, reproduced value, difference, layer where it
   diverged, root cause, and the query used (template: `references/divergence-log.md`).
7. Root cause found: record it in the right knowledge article (skill `knowledge-base`);
   definition problems go to the metric card (skill `metric-card`).

Formal validation work follows `new-request`; a one-off check follows `quick-check`.
Integrity of the data extracted by your own script follows `data-integrity-tdd`; query
cost follows `sql-performance` (data engineering).

## Routes

| If the task is... | Read |
|-------------------|------|
| Logging results and root causes; common causes of divergence | `references/divergence-log.md` |
| Input format of the comparison script | `python scripts/compare_numbers.py --help` |
