# Detailed query rules

## Projection
- List the consumed columns. `SELECT * EXCEPT (...)` is still a wide projection and needs a reason.
- `COUNT(*)` is fine when the row count is the metric.
- "Is there at least one row?" -> `EXISTS`, not an exact count (unless the total is required).
- Do in SQL what `WHERE`, `GROUP BY`, `CASE`, `SUM`, `COUNT`, `MIN`, `MAX` can do; do not ship raw rows to pandas.
- Remove columns, joins, sorts and computations nobody consumes; do not rely on the optimizer to prune them.

## Prunable filters
- Filter before joins/aggregations when semantics allow. In a `LEFT JOIN`, moving a predicate between `ON` and `WHERE` changes which rows survive.
- Half-open ranges: `ts >= :start AND ts < :end` (no lost last second).
- Avoid `DATE(col)`, `CAST(col)`, `LOWER(col)` or arithmetic on the filtered column; confirm pruning / index scan in the plan.
- Join keys with compatible types; do not cast both sides at runtime instead of fixing the model.
- Avoid leading-wildcard `LIKE '%x'` on large tables.

## Joins, aggregations, ordering
- Declare each side's grain, test key uniqueness, compare row and key counts before/after.
- Project and filter each input before the join; pre-aggregate when detail is not needed.
- With many joins on distributed engines, join the smaller inputs first and confirm in the plan.
- Avoid `CROSS JOIN`, global sorts and wide windows; keep only the partitions/order the rule needs.
- Prefer a window function over a self-join.
- Top-N: use the engine's top-N path; do not sort everything to discard most of it.
- A CTE organizes code; it does not guarantee materialization or single execution. Check the plan when a heavy CTE is reused.

## Plan, order, indexes
- Text order of tables/CTEs is not physical order; the optimizer reorders. Read the plan.
- Logical order (FROM/JOIN, WHERE, GROUP BY, HAVING, SELECT, DISTINCT, ORDER BY, LIMIT) is about correctness; the physical plan is the engine's choice.
- Look for unexpected full scans, estimate vs actual gaps, late filters, big shuffles/sorts, spill, skew, row explosion.
- Weigh total workload cost: duration x frequency, concurrency, rows examined vs returned, bytes read vs delivered. A short query run thousands of times can matter more than a rare long one.
- Composite index design comes from the workload: equality predicates, first range, order/group, covering, left prefix. Do not apply "most selective first" blindly.
- Change one variable at a time and compare plan, result and metrics; one wall-clock run is not evidence.
