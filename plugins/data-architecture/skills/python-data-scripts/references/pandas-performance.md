# pandas performance and memory

## Measure first
- Time phases with `time.perf_counter()`; `cProfile` for hot functions, `timeit` for micro cases, `tracemalloc` for allocations.
- Use representative data; set a "good enough" target first, then stop optimizing.
- Algorithm, I/O and volume beat syntax tweaks.

## Process less, avoid row loops
- Filter and aggregate in the database; on file reads use `usecols`, `dtype`, `parse_dates`.
- Prefer vectorized ops, masks, `groupby`, `merge`, `map`, NumPy. Vectorized string ops can still be slow and memory-hungry: measure.
- No `iterrows` on real workloads; if a loop is unavoidable, `itertuples(index=False)` with a tiny body.
- A loop over a few rows of a deliverable (formatting, rendering) is fine; the `iterrows` ban is for real volume.
- `apply(axis=1)` is not vectorization.
- Replace repeated lookups and nested loops with `dict`, `set`, index, `merge` or pre-aggregation.
- Top-N: `nlargest` / `nsmallest` after checking nulls and ties.
- No `pd.concat` in a loop: collect batches in a list only if the total fits comfortably; otherwise write incrementally.

## Memory, types, cache
- Inspect `df.info(memory_usage="deep")`; downcast only after validating ranges, precision and nulls.
- `category` for repetitive low-cardinality text; it hurts when values are mostly unique.
- Keep only needed columns in intermediates; avoid chains of defensive copies.
- Bigger than memory: chunked reads with incremental map/reduce aggregates; measure the real peak.
- Intermediate cache in Parquet (`to_parquet(index=False)`, `read_parquet(columns=[...])`): keeps types, IDs stay `str`. CSV/XLSX for deliverables and small caches.
- Do not add a heavy dependency without a measured gain.
- Do not parallelize by reflex: it raises memory and source load; only after profiling and within source limits.
