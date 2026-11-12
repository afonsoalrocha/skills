# Choosing status and maturity

## Status decision

Stop at the first row that applies.

| Situation | Status |
|-----------|--------|
| The data needed does not exist, or is not reliable at the grain asked | `blocked` (write the question and the reason) |
| Definition not yet approved by the owner, or reconciliation not done or out of tolerance, or the period is not mature | `indicative` |
| Definition approved, checks pass, reconciles with an independent source within tolerance | `certified` |

Downgrading is normal: when a source changes or a reconciliation fails, move the card down
and append the reason to `history`. Upgrading requires the owner's explicit approval.

## Maturity (metric maturity)

Some metrics are only readable after time passes: a repurchase rate needs the repurchase
window to close; a funnel's last step lags the first. `maturity_days` is the number of
days after a period ends before that period may be read as final.

- Top-of-funnel counts are usually readable at once; outcomes further down need longer.
- A period younger than `maturity_days` is shown as indicative or left out, never mixed
  with mature periods without a label.
- The value comes from the owner or from observed lag in the data, recorded in `history`.

## Reconciliation

Name one independent total the metric must match (for example the transactional system
behind the warehouse) and an explicit tolerance. Compare with that tolerance, never with
exact equality for currency values.
