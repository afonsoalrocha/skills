# data-analysis

Skills for defining a metric, checking a number, exploring an unfamiliar source, and recording what the work taught.

| Skill | What it is for |
|---|---|
| [quick-check](skills/quick-check/SKILL.md) | Answer a small ad hoc question and leave a reproducible trail. |
| [metric-card](skills/metric-card/SKILL.md) | Own a metric's meaning, status, maturity, and history. |
| [dashboard-validation](skills/dashboard-validation/SKILL.md) | Reproduce each dashboard number and log where it diverges. |
| [explore-unknown-source](skills/explore-unknown-source/SKILL.md) | Back claims about an unfamiliar source with profiles and a link test. |
| [knowledge-base](skills/knowledge-base/SKILL.md) | Keep durable project knowledge in `knowledge/` and its index. |
| [aws-quicksight](skills/aws-quicksight/SKILL.md) | Inspect and edit QuickSight assets, read-only unless approved. |
| [bi-assets-as-code](skills/bi-assets-as-code/SKILL.md) | Version published BI assets under `products/`. |

The procedure lives in each skill. This page only points at them.

## Requirements

`check_knowledge.py` and `validate_assets.py` need PyYAML. `quick_check.py`, `compare_numbers.py`, and `profile_sql.py` use the Python standard library only.
