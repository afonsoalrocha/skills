# Project setup

- Configure each layer in `dbt_project.yml` (schema and materialization per folder); do not live with global defaults.
- A `generate_schema_name` macro keeps dev and prod schemas predictable.
- Staging folders per source; intermediate and marts per business domain.
- Do not over-engineer staging on day one: bring only the columns you need, grow later.
- `sources.yml` per source with `loaded_at_field` and freshness thresholds.
- Pre-commit: SQLFluff (SQL style), yamllint, `check_naming.py`; convention beats tests that check cosmetics (e.g. "column is upper case").
- CI on every PR: `dbt build --select state:modified+` against a CI schema, plus the leak gate before anything public (skill `leak-gate`).
- PR checklist includes "I ran the data tests" and a note on which marts changed.
- A simple scheduler (CI cron) is enough at the start; an orchestrator comes when dependencies outside dbt appear.
- One canonical dataset per business concept if the goal is self-serve or AI agents; agents read model and column docs, so write them.
- Extend beyond three layers only with a clear consumer (semantic layer, reverse ETL, reporting).
