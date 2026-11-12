# data-architecture

Skills for checking data, modeling it, and keeping private material out of a public tree.

| Skill | What it is for |
|---|---|
| [data-integrity-tdd](skills/data-integrity-tdd/SKILL.md) | Write the data validator first, and conclude only when it passes. |
| [sql-performance](skills/sql-performance/SKILL.md) | Read less data: project, filter, inspect the plan, and page by key. |
| [production-db-readonly](skills/production-db-readonly/SKILL.md) | Query production MySQL or PostgreSQL read-only, in that database's dialect. |
| [databricks-workspace](skills/databricks-workspace/SKILL.md) | Query Databricks and move workspace files with the CLI or a SQL client. |
| [athena-queries](skills/athena-queries/SKILL.md) | Query Athena or Trino with metadata, a byte budget, and safe result reads. |
| [recurring-pipelines](skills/recurring-pipelines/SKILL.md) | Create or operate a recurring data job that repeats safely. |
| [python-data-scripts](skills/python-data-scripts/SKILL.md) | Write Python data scripts with typed identifiers, time zones, and atomic output. |
| [dbt-layered-modeling](skills/dbt-layered-modeling/SKILL.md) | Place each dbt model in a layer, with a name, a key, and a materialization. |
| [data-quality-gates](skills/data-quality-gates/SKILL.md) | Choose quality checks, and decide which ones block publication. |
| [data-contracts](skills/data-contracts/SKILL.md) | Agree and enforce the schema, grain, freshness, and meaning of a shared dataset. |
| [leak-gate](skills/leak-gate/SKILL.md) | Block publication when a private term or a secret is present. |

The procedure lives in each skill. This page only points at them. Names and areas are indexed in the repository [README](../../README.md).
