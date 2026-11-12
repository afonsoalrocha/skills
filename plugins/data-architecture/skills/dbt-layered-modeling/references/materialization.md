# Materialization and performance

- Default: staging and intermediate as views (or ephemeral), marts as tables; a slow view becomes a table.
- Heavy models reused by many children become tables.
- Full refresh first. Incremental only when build time or cost demands it; then define `unique_key`, `on_schema_change`, a late-arriving data lookback and a backfill plan.
- Check how `is_incremental()` filters behave on your engine: a filter that prunes on one warehouse can full-scan on another. Read the compiled SQL and the plan (skill `sql-performance`).
- Partition / cluster marts on the columns consumers filter by.
- Limit data in dev: filter recent dates when `target.name == 'dev'` (or a var) so iterations are cheap.
- Watch runtime per model and "modelnecks" (one slow model blocking the DAG); use tags/selectors to build slices.
- Avoid needless `ORDER BY` in models; prefer window functions to self-joins.
