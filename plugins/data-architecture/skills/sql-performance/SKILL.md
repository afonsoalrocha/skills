---
name: sql-performance
description: "Use before writing or reviewing any SQL query, including quick exploration, on any engine (Spark/Databricks, Trino/Athena, MySQL, PostgreSQL, warehouses): minimal projection, prunable filters, join grain, EXPLAIN before heavy reads, keyset extraction."
---

# SQL performance

Optimize the amount of data read, moved and materialized first; syntax second. Never
trade correctness for speed: keep a baseline and prove the faster version preserves
counts, keys, nulls, totals and grain (skill `data-integrity-tdd`).
Evidence order: semantic correctness > documented engine behavior > measured plan and
metrics > expert heuristic. Learn your own engine: the same SQL costs differently elsewhere.

## Invariants

- No `SELECT *` in extracts, joins, reused CTEs, final tables or shipped code (ad-hoc peek at a narrow source with a filter and small `LIMIT` is the only exception).
- Selective filters before joins and aggregations; half-open ranges (`>= :start AND < :end`).
- No function wrapped around a filtered column when a range or normalized value works.
- Declare the grain of each join side and test key uniqueness first; compare counts before/after.
- Never use `DISTINCT` to hide a join explosion.
- `EXISTS` / semi join to test existence; `UNION ALL` when dedup is not required.
- No `LIMIT/OFFSET` paging on large tables: date ranges or keyset (`id > :last ORDER BY id LIMIT :n`) with a checkpoint.
- `LIMIT` protects output; it does not replace `WHERE` and on many engines does not cut the scan.
- Nothing that executes the query in production (`EXPLAIN ANALYZE`) without weighing cost and risk.
- No index, `ANALYZE`/`OPTIMIZE`, hint or layout change in production without plan evidence, a benchmark and owner/DBA approval.
- Parameterize values; never interpolate user input into SQL.

## Flow

1. **Contract:** source, dialect, grain, output columns, window, expected volume.
2. **Metadata and cache first:** discover columns, keys and partitions without scanning.
3. **Reduce at the source:** project, filter early, aggregate in the engine, not in pandas.
4. **Representative sample:** short window or known keys.
5. **Plan before a heavy read** (engine `EXPLAIN`).
6. **Measure end to end** (engine, transfer, transform, write); more than one run when cache matters.
7. **Scale the window gradually** after result, cardinality and plan are validated.

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| Writing/reviewing a query in detail (projection, filters, joins, logical vs physical order, indexes, paging) | `references/query-rules.md` |
| Reading a plan: EXPLAIN / profile per engine (Spark, Trino, MySQL, PostgreSQL) | `references/explain-by-engine.md` |
| Profiling a huge partitioned table (pruning, sampling, approximate distinct, sentinels) | `references/large-table-profiling.md` |
| Extracting a large result in batches with checkpoints | `references/keyset-extraction.md` |
| Justifying a rule with official docs | `references/sources.md` |

## Review checklist

- [ ] Source, dialect, grain, window and volume explicit.
- [ ] No persistent `SELECT *`; projection, filters, aggregation reduce at the source.
- [ ] Half-open time filters that keep pruning / index use.
- [ ] Join key cardinality and types validated.
- [ ] Heavy query: plan inspected, run measured (frequency, rows/bytes, cache).
- [ ] Large extract is incremental, no offset.
- [ ] Result reconciled with the baseline.
