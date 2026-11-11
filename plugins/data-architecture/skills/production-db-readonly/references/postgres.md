# PostgreSQL route

- Placeholders: `%s` (psycopg) or named `%(name)s`; never f-strings.
- Session safety: `SET statement_timeout = '60s';` and run inside `BEGIN READ ONLY;` / `SET default_transaction_read_only = on;`.
- Always schema-qualify: `<schema>.<table>`; the default database name is configuration, not code.
- Metadata: `information_schema.columns`, `pg_indexes`, `pg_class.reltuples` (estimate only).
- Plan: `EXPLAIN (FORMAT JSON)`; `EXPLAIN (ANALYZE, BUFFERS)` executes, only with bounded risk.
- Large reads: server-side (named) cursor with `fetchmany`, or keyset paging (skill `sql-performance`).
- Timestamps: know whether the column is `timestamp` or `timestamptz`; convert explicitly.

```python
df = execute_sql(
    "SELECT COUNT(*) AS total FROM <schema>.<table> WHERE created_at >= %s AND created_at < %s",
    params=("2026-01-01", "2026-02-01"),
)
```
