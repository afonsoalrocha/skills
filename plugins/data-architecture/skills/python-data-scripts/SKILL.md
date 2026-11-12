---
name: python-data-scripts
description: "Use before writing or reviewing any Python data script (extraction, pandas transforms, deliverables, recurring jobs), including quick exploration: structure, typed IDs, dates and time zones, network errors, atomic output, validated joins, secrets."
---

# Python data scripts

Applies to every new or changed script, exploration included. Correctness before speed:
keep a baseline and prove counts, keys, nulls, totals and grain survive any optimization.
Reduce at the source first (skill `sql-performance`); validating the data itself is
skill `data-integrity-tdd`.

## Invariants

- **Shape:** extract -> validate -> transform -> deliver. Transforms are pure (DataFrame in, DataFrame out); I/O at the edges, in `main()` with `argparse`.
- **Connections:** only through the project's connector modules; no ad-hoc driver code in analysis scripts.
- **Imports:** install the project as a package (`pip install -e .`) and import qualified; no `sys.path.insert` in new code.
- **IDs:** always `str` (`dtype=str`); declare `dtype` and `parse_dates` on every file read.
- **Gaps:** no `fillna(0)` on a metric whose source has gaps; `groupby(dropna=False)` when nulls matter.
- **Dates:** explicit `ZoneInfo`; storage in UTC, business in a declared local zone, the zone in the column name (`created_at_utc`); half-open windows; no naive `datetime.now()`.
- **Errors:** never bare `except:` or `except Exception: pass` (turns 403/timeout into "no data"). Catch specific errors, retry with backoff, fail loudly; broad catch only at `main()` to mark `partial` and exit non-zero.
- **Output:** write `<name>.partial` then `os.replace`; a manifest next to it (source, window, rows, hash, generated_at); no implicit "today" in names or windows.
- **pandas:** `merge(..., validate=...)` and check `shape`; assign with `.loc`; never `drop_duplicates()` to hide a join explosion; no `iterrows` or `pd.concat` in loops.
- **Secrets/config:** environment or `.env` loaded at the edge; no tokens, tenant IDs or user home paths in code.
- **Terminal/portability:** `pathlib`, explicit `encoding="utf-8"` (`utf-8-sig` for CSV opened in spreadsheets), ASCII status words, `subprocess.run([...], check=True, timeout=...)`, never `shell=True` with interpolation.

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| Script structure, packaging/imports, config and argparse, logging, subprocess, pytest | `references/structure-and-env.md` |
| Reading/writing with IDs, dates and time zones, network failures, atomic output with manifest, joins | `references/ids-dates-output.md` |
| Volume matters: measuring, avoiding row loops, memory, chunks, Parquet, parallelism | `references/pandas-performance.md` |
| Atomic write plus manifest helper | `scripts/atomic_output.py` (requires pandas, outside the standard library; Parquet also needs pyarrow or fastparquet) |
| Justifying a rule with official docs | `references/sources.md` |

## Review checklist

- [ ] Extract, validate, transform, deliver separated; transform is pure.
- [ ] Qualified imports; connections via connector modules.
- [ ] IDs `str`; dtypes and dates declared; no `fillna(0)` on source gaps.
- [ ] Explicit time zones and half-open windows.
- [ ] No swallowed exceptions; network failure never becomes "no data".
- [ ] Joins with `validate=` and shape checked.
- [ ] Output via `.partial` + `os.replace` with manifest; no secrets or user paths.
- [ ] Volume relevant: time per phase and peak memory measured.
- [ ] Result reconciled with the baseline.
