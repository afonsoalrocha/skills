# MySQL route

- Placeholders: `%s` with a params tuple (driver-dependent); never string formatting.
- Session safety: `SET SESSION MAX_EXECUTION_TIME = 60000;` (milliseconds, SELECT only) and `SET SESSION TRANSACTION READ ONLY;`.
- Metadata without scanning: `information_schema.COLUMNS`, `information_schema.STATISTICS` (indexes), `SHOW CREATE TABLE`.
- `information_schema.TABLES.TABLE_ROWS` is an estimate for InnoDB, not a count.
- Plan: `EXPLAIN FORMAT=JSON`; watch `type=ALL`, `rows`, `filtered`, `key`.
- Date ranges: compare the raw column (`created_at >= %s AND created_at < %s`) so the index is usable; `DATE(created_at) = ...` prevents it.
- Character set / collation differences across joined columns can block index use.

```python
df = execute_sql(
    "SELECT COUNT(*) AS total FROM <schema>.<table> WHERE created_at >= %s AND created_at < %s",
    params=("2026-01-01", "2026-02-01"),
    target="replica",
)
```
