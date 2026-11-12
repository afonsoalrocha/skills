---
name: data-integrity-tdd
description: "Use before any analysis, extraction, integration or recurring job that produces data. Write the data validator before the script, run it on the data, and only conclude if it passes; otherwise label the result partial or blocked."
---

# Data integrity, test first

The validator proves the data is sound at each hop (source, extract, transform, deliver).
It is not a unit test of the code. Expectations come from the contract, never from what
the data "seems" to show.

## Invariants

- Write the validator before the analysis or pipeline script, from the contract.
- Run it twice: on the extract (before transforming) and on the result (before concluding).
- A failed check on the extract stops the flow; never "fix" it downstream in the transform.
- A failed check means no conclusion: label the result `partial` or `blocked` with the reason.
- Grain is unique before any join; result row count matches the source count.
- Time windows are half-open (`>= start AND < end`) in a declared time zone.
- Absence is not zero: a source gap becomes NULL / unavailable, never `0`.
- An access failure (403, proxy, SSO, timeout) is not "no data": retry, then fail loudly.
- IDs are strings (leading zeros survive); money is compared with an explicit tolerance, never `==`.
- Saying "the API/tool cannot do X" requires reading the docs or testing the documented name.
- A negative claim ("there is none", "never carries", "does not exist") needs a sweep of the whole universe (all events, columns, periods, not only those the script uses), with the swept scope written next to the claim; without the sweep, write "not verified".

## Flow

1. **Contract:** source and dialect, grain, key, window and time zone, critical columns,
   where the expected total comes from (an upstream source), tolerance.
   If a formal contract exists, start from it (skill `data-contracts`).
2. **Validator first:** `NN_validate_<topic>.py` (or pytest for a pipeline), next to the
   script it validates. Start from `scripts/validator_template.py`.
3. **Run on both points;** collect every failure, do not stop at the first.
4. **Record** status `complete` | `partial` | `blocked` and the checks that ran, in the
   request README or the output manifest.

## Proportionality

| Work type | Minimum |
|-----------|---------|
| Quick check / exploration | 3 checks: unique grain, count vs source, window and time zone |
| Analysis or data product | full set plus reconciliation with the upstream source; validator versioned |
| Recurring pipeline | validator runs every execution; integrity failure blocks, value anomaly warns (skill `data-quality-gates`) |

Does not apply to admin work with no analytical data (access requests, docs, tickets).

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| Building the full check set (reconciliation, slices, sentinels, discriminating columns, compared version) and known traps | `references/checks.md` |
| Writing the validator in Python (OK/ERROR/WARN output, exit code, file fixtures) | `references/implementation.md` |
| Starting a validator from a template | `scripts/validator_template.py` (requires pandas, outside the standard library) |

Related: SQL that feeds the check, skill `sql-performance`; Python style, skill `python-data-scripts`.
