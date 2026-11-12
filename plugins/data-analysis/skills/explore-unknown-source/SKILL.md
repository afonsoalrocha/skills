---
name: explore-unknown-source
description: "Map an unfamiliar table, view, API or export before relying on it: what each field really contains, how it links to other data, what one row means. Use before claiming a join, a missing field or a grain. Analytical side only; data tests and query cost belong to data engineering."
---

# Explore an unknown source

Exploration exists to back **claims** about a source: "A links to B through column C",
"field F is not available", "one row is one event". Each claim needs evidence from values,
because labels and types are written by someone else and are often wrong or vague.

## 1. Profile all fields, not the promising ones

Get the schema from metadata, then run one profile per table over a short recent window:
fill rate, distinct count and a few short example values for every field.
`python scripts/profile_sql.py profile ...` (paths relative to this skill) writes that SQL;
it splits wide tables into blocks and leaves personal-data fields out. On big or
partitioned tables, the pruning and sampling discipline of `sql-performance`
(`references/large-table-profiling.md`) applies; it is not repeated here.

## 2. Interpret the profile

| What you see | What it probably means | What to do next |
|--------------|------------------------|-----------------|
| Values shaped like another table's identifiers, whatever the field is called | a hidden link | key test (step 3) |
| A single value in the whole window | describes the extract or its origin, not the rows | do not split or count by it |
| As many values as rows | a row identifier | confirm uniqueness on a longer window |
| Fewer values than rows | either genuine repeats or a view that fans rows out | compare row count with distinct-id count |
| Filled for only part of the rows | a field that appears at a certain point in the record's life | compare fill rate per status or stage before calling it broken |

## 3. Prove the claims, then write the source map

- Every candidate link gets a key test in both directions: coverage on each side,
  cardinality (one-to-one or one-to-many) and duplicate keys.
  `python scripts/profile_sql.py key-test ...` writes it.
- Grain: rows per identifier; when a view fans out, count distinct identifiers.
- The source map lists, per field, what it holds; per link, its test result; and a
  **coverage note** naming the fields actually inspected. A negative claim ("there is no
  link") holds only for inspected fields; everything else is unknown, not absent.

## Privacy

Personal fields (names, contact data, documents, addresses, card fragments, free-text
payloads) are excluded from examples by name pattern; for JSON fields read only the keys.
Customer identifiers may appear inside counts, never as returned values.

## Pitfalls

- Short windows miss rare states: add a breakdown by status.
- Sentinels and text-encoded nulls: `data-integrity-tdd`.
- Output aliases that clash with reserved words or real column names fail with vague errors.
- A permission error or timeout says nothing about whether data exists.

## Routes

| If the task is... | Read |
|-------------------|------|
| Query shapes per dialect, key-test logic, worked synthetic example | `references/profile-and-key-test.md` |
| Script options | `python scripts/profile_sql.py --help` |

Meanings that define a metric go to `metric-card`; durable findings to `knowledge-base`.
