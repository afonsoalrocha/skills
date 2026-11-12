---
name: athena-queries
description: "Use when querying Amazon Athena or another Trino engine: discovering catalogs, databases, tables and partitions, planning a query, checking bytes scanned and cost, and reading results safely."
---

# Athena / Trino queries

Athena bills per byte scanned, so cost control is part of correctness. Dialect is
Trino (Athena engine v3), not Spark and not MySQL.

## Auth

- Use the project's Athena client with a named AWS profile (`AWS_PROFILE=my_profile`,
  SSO login) and an explicit workgroup from config; no access keys in `.env` or code.
- Never switch profile, role or workgroup to get around `AccessDenied`: report the
  action and resource, and wait for the grant.

## Cost

- Discover catalog, database, columns and partition keys via the paginated metadata
  APIs (`list_*`, `get_table_metadata`) before reading data.
- Project only the columns you need and always filter on partition keys; `LIMIT`
  does not limit the scan.
- `EXPLAIN (TYPE IO)` before heavy reads; `EXPLAIN ANALYZE` runs (and bills) the query.
- Record `DataScannedInBytes`, `EngineExecutionTimeInMillis` and `QueryExecutionId`
  with every result (for example in `DataFrame.attrs` or the manifest).
- Check for a cached extract of the same query and window before re-scanning.

## Results

- Results arrive as strings/None: cast types explicitly and keep decimals as
  `Decimal`, not float, until the last step.
- Large results: iterate result pages in batches; never load an unknown volume at once.
- A `max_rows` cap protects memory, not cost.
- A client timeout must call `StopQueryExecution`.
- Normal results land in the workgroup's S3 output location: treat it as data, with retention.

## Safety

- No DDL/DML, CTAS, `UNLOAD` or workgroup changes without explicit scope; a first-verb
  check is not IAM.
- Do not infer freshness or CDC behavior of a table without evidence (partition listing,
  load metadata).

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| Estimating and controlling scan cost (partition projection, columnar formats, budgets) | `references/cost-control.md` |
| Client patterns: start/poll/cancel, paging results, type casting, metadata pagination | `references/client-patterns.md` |
| General plan reading and query rules | skill `sql-performance` |
