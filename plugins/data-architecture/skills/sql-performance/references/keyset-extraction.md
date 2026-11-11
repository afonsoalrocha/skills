# Paging a large extract without OFFSET

`LIMIT` plus `OFFSET` is a poor way to page a large table: high offsets reread and
throw away earlier rows, and without a unique `ORDER BY` a page can repeat or skip
rows. Prefer not to extract full detail at all — project fewer columns, or aggregate
at the source — and only page when that detail is required.

Page on a half-open date window, or on a stable increasing key, and keep a
checkpoint of the last key (or window) successfully written. On resume, start
after that checkpoint and dedupe by the same key. Bound memory: write each batch
out; do not grow an unbounded in-memory frame. Some SQL APIs cap inline results
silently, so assert the count of every batch and of the total.

```python
resume_from = load_checkpoint()  # last key written, or None
key = resume_from if resume_from is not None else 0
page_size = 50_000

while True:
    rows = run_query(
        "SELECT id, needed_col FROM <catalog>.<schema>.<table> "
        "WHERE id > %(key)s ORDER BY id LIMIT %(page_size)s",
        params={"key": key, "page_size": page_size},
    )
    if rows.empty:
        break
    write_batch(rows)
    key = int(rows["id"].iloc[-1])
    save_checkpoint(key)
```

Parameterize the bound and the page size; do not interpolate them into the SQL
string. The same idea applies to date windows: `ts >= :start AND ts < :end`, then
advance `:start`.
