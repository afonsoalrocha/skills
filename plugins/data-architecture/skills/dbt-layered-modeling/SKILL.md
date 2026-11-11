---
name: dbt-layered-modeling
description: "Use when designing, adding or reviewing dbt models or a dbt project layout: choosing the layer (staging, intermediate, mart), naming, materialization, keys and where business logic should live."
---

# dbt layered modeling

Goal: turn messy source data into numbers people can trust, in a system of models that
survives changing business rules. Think in systems, not tools: dbt is only the T in ELT;
ingestion and orchestration live elsewhere. Business logic lives in dbt; the BI tool only presents.

## Invariants

- The layer is chosen by purpose and consumers, never by how complex the SQL looks.
- **staging:** one model per source table, cleans and aligns the source (rename, cast, timestamps to UTC, units); no joins across sources, no business rules.
- **intermediate:** small reusable building blocks shared by more than one output; never "the final table with all the logic".
- **mart:** answers a business question for a stakeholder; named for the business entity or question.
- One model, one responsibility. If you need "and" to describe it, split it.
- Shift left: transform as early as possible (ideally staging) so downstream stays DRY.
- Every model has a tested primary key; no natural key means a surrogate key from `dbt_utils.generate_surrogate_key`, never a hand-rolled hash.
- Naming is an architecture decision: follow `references/naming.md` and check it with `scripts/check_naming.py`.
- Sources are declared in `sources.yml` with freshness; models reference `source()` / `ref()`, never hard-coded relation names.
- Document inputs (staging), outputs (marts) and any new intermediate logic; comments explain why, for humans and AI agents alike.
- Start simple: views and full refresh first; incremental only when volume justifies the backfill and schema-change cost.
- Learn your engine: the same incremental or partition config can full-scan on another warehouse.
- Small PRs (a few models, one concern); every model change is reviewed and tested in CI.
- Do not model what you do not understand yet: profile the source before writing staging.
- AI drafts and reviews models; a human owns the logic and verifies the numbers.

## Design flow

1. Start from the mart: the business question, its grain and its consumer.
2. Walk back to sources; reuse existing models before creating new ones (search docs first).
3. Pick the layer per piece of logic by purpose (table below), then name it.
4. Weigh the four pillars: **scale of change** (can metrics/rules change fast?), **reuse** (logic written once?), **performance/cost** (build and query time), **quality** (tests that protect meaning, skill `data-quality-gates`).
5. Add contracts on marts others depend on (skill `data-contracts`).

| Logic | Layer |
|-------|-------|
| Source-specific cleanup, casting, renaming, dedupe of source rows | staging |
| Logic reused by two or more outputs (sessionization, currency conversion, complete periods) | intermediate |
| Stakeholder-ready table answering one question | mart |
| Reconciliation and integrity views | audit (optional layer) |
| Metric definitions consumed by BI/agents | semantic layer / metrics, not the dashboard |

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| Naming models, folders, columns and keys | `references/naming.md` |
| Choosing materialization, incremental strategy, dev data limits, performance | `references/materialization.md` |
| Setting up or restructuring a project (folders, `dbt_project.yml` per layer, CI, pre-commit) | `references/project-setup.md` |
| Checking model names against the convention (`--single-source` allows `stg_<entity>`) | `scripts/check_naming.py` |
