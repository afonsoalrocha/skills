# `asset.yaml` and `CHANGELOG.md`

```yaml
id: monthly-sales-dashboard        # equals the folder name
type: dashboard                    # dashboard | dataset | semantic_model | workspace | app | ...
name: Monthly sales
owner: role
status: certified                  # certified | indicative | blocked (follows its metrics)
tool: quicksight                   # or another BI tool
resource_id: dash-0001             # id inside the tool; unique across all assets
source_request: "001"              # request that created it, if any
metrics: [delivered_orders, product_revenue]   # metric card ids
relationships:
  - type: uses_dataset
    target: monthly-sales-dataset
# the dataset manifest declares the inverse:
#   - type: used_by_dashboard
#     target: monthly-sales-dashboard
publish:
  script: publish.py
  last_published: 2026-01-15
```

Inverse relationship pairs used by the validator:
`uses_dataset`/`used_by_dashboard`, `in_container`/`contains`, `feeds`/`fed_by`.

Changelog entry (append at the top or bottom, consistently, never edit old entries):

```markdown
## 2026-01-15 — monthly-sales-dataset
- Why: request 001 needs freight split.
- Change: added column freight_value at the end.
- Validation: refresh completed, row count equal to the previous load, old columns unchanged.
- Result: published; dashboard visuals rechecked.
```
