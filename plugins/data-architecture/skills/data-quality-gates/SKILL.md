---
name: data-quality-gates
description: "Use when deciding which data quality checks a model, source or pipeline needs and whether each one blocks publication or only warns: freshness, schema, keys, volume anomalies and business-rule tests."
---

# Data quality gates: block vs warn

Green generic tests protect the shape of a table, not the meaning of the numbers. Quality
means the data meets what consumers expect, so gates cover four things: freshness,
contracts (schema and keys), anomalies and business rules. Shift left: catch problems at
the source and staging, where the damage is smallest.

## Invariants

- Every gate has an explicit severity: `block` stops publication; `warn` is recorded and publication continues.
- Block when publishing would be wrong: missing input, stale source past its threshold, broken contract, duplicate keys, count mismatch vs source, failed business rule on a critical column.
- Warn when the value is surprising but possible: volume or metric anomaly, minor nulls in a non-critical column, freshness near the threshold.
- A gate result is data: gate name, severity, state (`pass` | `warn` | `block`), message; written to the run manifest.
- Gates are deterministic code (dbt tests, SQL assertions, Python checks), not an agent's judgment.
- Test the primary key at the first layer it exists; downstream, test only new or transformed columns, plus redundant checks on business-critical mart columns.
- Prefer conventions and code review over cosmetic tests (case, formatting); they bloat the suite and cost money.
- Freshness runs before the build, with per-source thresholds and a filter so it does not scan the whole table.
- Absence is not zero and an access error is not "no data" (skill `data-integrity-tdd`).
- Status and definition of a metric live in the `metric-card` skill (data-analysis plugin). This skill only maps a gate result to a status: a failed `block` gate means the metric is not published as `certified` that run.
- Never weaken or delete a gate to make a run pass; change severity only with the owner's agreement, in a reviewed change.

## Choosing gates (test-informed, not test-everything)

| Concern | Typical gate | Default severity |
|---------|--------------|------------------|
| Freshness | `dbt source freshness`, max(loaded_at) vs threshold | block past error threshold, warn past warn threshold |
| Contract | columns and types, enforced model contract | block |
| Keys | `unique` + `not_null` on PK, relationships on FKs | block (PK), warn or block (FK) by criticality |
| Completeness | row count vs source, missing dates/partitions | block |
| Anomaly | volume or metric outside expected band | warn |
| Business rule | singular test (e.g. no shipped order without items, no negative measures, no open period in a monthly mart) | block when critical |

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| Implementing gates in dbt (severity config, singular tests, freshness, store failures) | `references/dbt-gates.md` |
| Mapping a gate result to metric status (certified / indicative / blocked) | `references/metric-status.md` |
| A gate runner in Python with block/warn results and exit codes | `scripts/gates.py` |
| Writing the validator for a one-off analysis | skill `data-integrity-tdd` |
