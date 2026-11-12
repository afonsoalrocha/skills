# Divergence log

Save as `outputs/dashboard-validation.csv` (or `.md`) in the request or quick-check folder.

| number_id | visual | filters | period | dashboard_value | reproduced_value | diff | within_tolerance | layer_diverged | root_cause | query |
|-----------|--------|---------|--------|-----------------|------------------|------|------------------|----------------|------------|-------|

## Common causes (check in this order)

1. **Different filters or period**: default dashboard filters, hidden page filters, open
   period included, time zone cut (storage often in UTC, business in local time).
2. **Different definition**: the visual uses a column or formula that the metric card
   lists under `never_use`, or an older rule.
3. **Stale data**: the dashboard's extract or cache was refreshed before the last load.
4. **Grain and duplication**: a join multiplies rows; a view repeats an id; counting rows
   instead of distinct ids.
5. **Pre-computed totals**: a total row or subtotal summed again with its parts; slices
   that do not add to the total because of an "unknown" bucket.
6. **Absence treated as zero**, or zero treated as absence.
7. **Type issues**: ids read as numbers lose leading zeros and stop matching.
8. **Upstream defect**: the intermediate or source layer itself is wrong; hand over to the
   data-engineering owner with the evidence.

A divergence explained is a result. Record it even when the dashboard turns out right.
