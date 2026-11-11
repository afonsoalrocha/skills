# Metric card template

```yaml
id: metric_id                      # stable, snake_case, never reused
name: Business name
status: certified                  # certified | indicative | blocked
definition: One sentence a colleague outside the data team can repeat.
formula:
  numerator: count(distinct order_id)
  denominator: null
  aggregation: count_distinct
unit: orders                       # count, currency (which), ratio, percent, days
grain: the source row, and the rollup you publish
default_date_column: event_timestamp
time_zone: the business time zone used to cut periods
required_filters:
  - status = 'delivered'
allowed_dimensions:
  - name: month
    caution: ""
never_use:                         # columns or formulas that look right but are wrong
  - ""
maturity_days: 0                   # days until a period is readable
reconciliation_source: The independent total this metric must match, and tolerance.
owner: role of the person who decides the definition
decided_at: 2026-01-15
block_reason: null                 # required sentence when status is blocked
history:
  - "on": "2026-01-15"
    change: Initial definition.
    decided_by: role
```

Field notes:
- `required_filters` are part of the definition. A number without them is another metric.
- `allowed_dimensions.caution` says when a breakdown misleads (for example a dimension
  that is filled only after a later event).
- `never_use` exists to stop the next analyst from picking the obvious wrong column.
- `reconciliation_source` must be independent of the metric's own pipeline.
