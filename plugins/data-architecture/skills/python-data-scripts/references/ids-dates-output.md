# IDs, dates, errors, output, joins

## IDs and types
- Read every identifier (order, customer, product codes, national IDs) as `str`; never let pandas infer it (leading zeros lost, float, scientific notation).
- Write IDs as text in spreadsheets; never round-trip an ID CSV through a spreadsheet app.
- Absence is not zero: no `fillna(0)` on gapped metrics; `groupby(dropna=False)` when null keys matter.

## Dates and time zones
- Convert with explicit `ZoneInfo("<Area/City>")`; name columns with the zone (`created_at_utc`, `order_date_local`).
- Half-open windows (`>= start`, `< end`).
- Never compare naive and aware datetimes; never `tz_localize` without knowing the source zone.

## Errors and network
- Catch the specific exception, retry with bounded exponential backoff, then fail with a useful message.
- Broad `except Exception` only at the `main()` boundary: log, mark the result `partial`, exit non-zero.

## Reproducible output
- Write to `<name>.partial` in the same folder and `os.replace` at the end; delete the `.partial` on failure (see `scripts/atomic_output.py`).
- Write a manifest next to the output: source, window, rows, sha256, generated_at (UTC).
- Do not overwrite a valid cache without checking; no implicit "today" in names or windows.

## Joins and assignment
- `merge(validate="one_to_one" | "one_to_many" | "many_to_one")`, compare shapes before/after, `indicator=True` when row loss matters.
- Assign with `.loc`; avoid chained indexing and `inplace=True`.
