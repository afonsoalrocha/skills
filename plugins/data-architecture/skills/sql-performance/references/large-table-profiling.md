# Profiling a huge partitioned table

The aim is to learn what a large table holds without paying for a full scan. Do the
cheap work first, and only touch data inside a pruned slice.

Start on **one partition value**. Confirm that the filters, casts and questions are
right on that slice, then widen the window or add partitions.

Learn the shape from the catalog, not from a scan. `DESCRIBE` or the engine's
metadata APIs give columns, types, comments and partition keys at negligible cost.
Every later query must prune on those partition keys; an aggregation with no
partition predicate is not a viable profile.

Once the slice is chosen, look at real values: a short sample, or `TABLESAMPLE`
placed immediately after the table name (before `WHERE`; in Spark SQL, `TABLESAMPLE (n ROWS)` after the `WHERE` is a syntax error). That is usually enough
to see embedded JSON, sentinels and free-text patterns. Then run **one** aggregation
pass on the same slice: row count, approximate distinct counts, and null counts.
Exact `COUNT(DISTINCT)` across many columns forces heavy shuffles; prefer the
engine's HyperLogLog-style approx.

Frequency tables come last, and only for columns the profile showed are
low-cardinality. Several such `GROUP BY` queries can be submitted as one
`UNION ALL` to avoid a round trip each. Skip top-N on identifiers, timestamps
and wide free-text.

## What goes wrong

A large `LIMIT` inside a CTE is not a cheap sample: the engine may materialize
every column before it aggregates. Prefer a tiny sample or `TABLESAMPLE` in the
position the engine actually pushes down.

`IS NULL` will report a clean column when emptiness is stored as a value
(`'NULL'`, `0`, `-1`, `''`, all-zero strings). Read the frequent values and treat
those sentinels as empty in filters and checks.

A timeout in the local client often leaves the warehouse query running. Keep each
statement small, and cancel it explicitly on the cluster if the client gives up.
