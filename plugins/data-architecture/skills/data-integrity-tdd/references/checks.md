# Check catalog and known traps

Use these as a menu, not a fixed sequence. Pick the checks the question needs, write
them first, and record each result as `complete`, `partial` or `blocked`.

## Identity and grain

- Assert the declared key is unique before any join. Uniqueness is about the key
  you will join on, not about two rows looking alike on business attributes.
- Read identifiers as text (`str`). Numeric inference drops leading zeros and can
  merge values that are not the same key.
- Before splitting a result by a column, confirm it actually varies (`nunique() > 1`
  and a sensible share per value). A constant distinguishes nothing.

## Completeness and reconciliation

- The result's row count must equal `COUNT(*)` at the source under the same filter.
  Some clients truncate large inline results without raising an error; assert the count.
- Totals should match the next layer upstream, walking toward the source system.
  A BI semantic model or a dashboard visual is not the source of truth.
- Slices must sum to the total. Do not trust a precomputed "total" row.
  An "unknown" / "not set" bucket is a slice, not a row you may drop.

## Time, missingness and access

- Use full periods, a half-open interval, and a cut-off consistent with load time.
  A lake stored in UTC and a report in a local zone will disagree if you ignore the zone.
- Count nulls in critical columns and look for sentinels (`'NULL'`, `0`, `-1`, `''`,
  all-zero strings). `IS NULL` reports 0% when empty is encoded as a value.
- A period with no source coverage is NULL / unavailable, not zero. Filling gaps
  with 0 invents a drop.
- Retry on permission errors, proxy failures and timeouts; then fail. A network
  error is not evidence that the data is empty.

## Comparison and claims

- Declare which snapshot you are comparing (published version, extract of date X,
  load of date Y). A stale copy produces a false divergence.
- Claim a system "cannot" do something only after reading its docs or calling a
  documented parameter. A homemade parameter that errors proves nothing.

## Status labels

- `complete`: every blocking check passed.
- `partial`: the result is usable with a stated gap (for example one source missing
  a period); write the gap next to the number.
- `blocked`: a blocking check failed; nothing is concluded or published.
