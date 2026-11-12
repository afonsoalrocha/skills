# Plans by engine

## Spark SQL / Databricks SQL
- `EXPLAIN FORMATTED` for physical structure; `EXPLAIN COST` when statistics exist. After running, use the query profile (rows, time, memory, I/O, shuffle).
- Static `EXPLAIN` may not show the final plan after Adaptive Query Execution; check the final plan/profile.
- Look for partition pruning, data skipping, sensible broadcast, exchanges, spill, skew. Prefer native SQL functions over UDFs.
- Do not force broadcast, repartition, cache or salting by default; only when size, reuse or key distribution justify it.
- Statistics and layout (`ANALYZE TABLE`, clustering, optimize) are engineering changes, not analysis side effects.

## Trino / Athena
- `EXPLAIN (TYPE IO)` estimates the data read per table/partition without running; use it before heavy reads.
- `EXPLAIN ANALYZE` executes the query (and bills the scan).
- Partition and column projection drive cost; `LIMIT` does not reduce the scan. See skill `athena-queries`.

## MySQL
- Start with `EXPLAIN FORMAT=JSON`: `key`, `rows`, `filtered`, join order, unexpected `type=ALL` on big tables.
- `EXPLAIN ANALYZE` executes the statement; only when the read is bounded and production load is acceptable.
- B-tree composite indexes: left prefix and selectivity. Avoid hints by default.

## PostgreSQL
- Start with `EXPLAIN (FORMAT JSON)` or `EXPLAIN (COSTS, VERBOSE)`.
- `EXPLAIN ANALYZE` executes; in production only after bounding risk; with approval, `BUFFERS` separates I/O from CPU/cache.
- Large gaps between estimated and actual rows suggest stale stats or correlated predicates; escalate to the owner/DBA.
