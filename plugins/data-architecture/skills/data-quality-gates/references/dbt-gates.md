# Gates in dbt

- Severity per test: `config: {severity: error}` blocks; `severity: warn` warns. Thresholds: `warn_if: ">0"`, `error_if: ">100"`.
- `dbt build` stops downstream models when a blocking test on a parent fails; that is the gate.
- Source freshness in `sources.yml`:
  ```yaml
  sources:
    - name: <source>
      loaded_at_field: _loaded_at
      freshness:
        warn_after: {count: 12, period: hour}
        error_after: {count: 24, period: hour}
        filter: _loaded_at >= current_date - 3
  ```
  Run `dbt source freshness` before `dbt build`.
- Golden source tests: expected columns (light contract), PK uniqueness/not null or surrogate, completeness of dates/partitions, relationships, volume anomaly (packages such as dbt-expectations or Elementary).
- Singular tests in `tests/` return failing rows; name them `assert_<rule>`.
- Unit tests (`unit_tests:` in YAML, dbt >= 1.8) protect transformation logic with fixed inputs; use them for tricky CASE/date logic, not for every column.
- `--store-failures` keeps failing rows for diagnosis.
- In CI: `dbt build --select state:modified+`; publish only if no `error` test failed.
