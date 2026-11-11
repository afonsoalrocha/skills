# Cost control

- Cost ~ bytes scanned. Columnar (Parquet/ORC) plus column projection plus partition pruning are the three levers.
- Check partition keys first; a filter on a non-partition column still scans every partition.
- With partition projection, the filter must match the projected format (e.g. `dt = '2026-11-01'` as string) or pruning silently fails.
- Run `EXPLAIN (TYPE IO)` and read the estimated input size per table; compare to a budget per query.
- Set a workgroup per-query data limit when you own the workgroup; otherwise enforce a client-side bytes budget using the IO estimate.
- After running, compare `DataScannedInBytes` with the estimate; a large gap means pruning did not happen.
- Many small files cost time, not bytes: report it to the table owner, do not "fix" with ad-hoc CTAS.
- Reuse results: Athena query result reuse (when enabled) or the project's local cache keyed by SQL text and window.
