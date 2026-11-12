---
name: data-contracts
description: "Use when a dataset is consumed by another team, model, dashboard or agent and its schema, grain, keys, freshness or semantics must be agreed, versioned and enforced, or when a producer wants to change such a dataset."
---

# Data contracts

A contract is the explicit promise a producer makes to consumers: what the dataset is,
at what grain, with which columns and types, how fresh, and what the values mean. It
turns "don't break my dashboard" into something a machine checks.

## Invariants

- Contract the boundaries, not every model: sources you ingest from, and marts or exports others consume.
- A contract states: owner, purpose, grain and primary key, columns with types/nullability/meaning, freshness SLA, allowed values or ranges for critical columns, version.
- The contract lives in the repo next to the model (YAML), versioned and reviewed like code.
- Enforce it in the build: schema enforcement (e.g. dbt model contracts) plus tests for keys, ranges and freshness (skill `data-quality-gates`); a broken contract blocks.
- Additive changes (new nullable column) are minor; removing/renaming a column, changing type, grain or meaning is breaking.
- Breaking changes ship as a new version with a deprecation window; the old version keeps working until consumers migrate.
- Semantics count as much as schema: a column whose meaning changes is a breaking change even if its type does not.
- Do not contract what you do not understand yet; profile the source first and start with a light contract (expected columns + PK), then tighten.
- Consumers are listed (dbt exposures or a consumers section) so impact is known before a change.
- Metric meaning and status live in the `metric-card` skill (data-analysis plugin). A contract may name the metrics a dataset feeds; it does not redefine them. Publishing gates that read the card are in `data-quality-gates`.

## Flow

1. Identify the boundary and its consumers.
2. Draft the contract from `references/contract-template.yaml`.
3. Agree with consumers on grain, keys, freshness and meaning of critical columns.
4. Enforce: model contract and tests in CI; freshness before builds.
5. Change: classify additive vs breaking with `scripts/contract_diff.py`; breaking means a new version.

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| Writing a contract file | `references/contract-template.yaml` |
| Enforcing in dbt (contract enforced, constraints, versions, exposures) | `references/dbt-contracts.md` |
| Contracts on ingested sources (expected columns, schema drift handling) | `references/source-contracts.md` |
| Classifying a schema change as additive or breaking | `scripts/contract_diff.py` (requires PyYAML, outside the standard library) |
