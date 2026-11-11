# Enforcing contracts in dbt

- `config: {contract: {enforced: true}}` on the model; every column listed with `data_type`. The build fails if the SQL output does not match.
- `constraints:` (`not_null`, `primary_key`, `check`) are enforced only where the platform supports them; back them with tests anyway.
- Model versions (`versions:` with `latest_version`) publish a breaking change as `v2` while `v1` stays for consumers; set `deprecation_date` on the old one.
- `access: public | protected | private` and groups mark which models are meant to be consumed.
- `exposures:` list dashboards, apps and agents that depend on a model, so `state:modified+` shows impact.
- Run contracts and tests in CI on every PR touching a contracted model.
