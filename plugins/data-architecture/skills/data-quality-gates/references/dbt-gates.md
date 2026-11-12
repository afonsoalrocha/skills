# Gates in dbt

- dbt `error` severity maps to gate `block`. dbt `warn` maps to gate `warn`. In test config, `severity: error` is the block gate and `severity: warn` is the warn gate. Thresholds: `warn_if: ">0"`, `error_if: ">100"`.
- `dbt build` stops downstream models when a blocking test on a parent fails; that is the gate.
- Source freshness in `sources.yml`. The counts below are placeholders; set the warn threshold, the error threshold, and the lookback per source:
  ```yaml
  sources:
    - name: <source>
      loaded_at_field: _loaded_at
      freshness:
        warn_after: {count: <warn_hours>, period: hour}
        error_after: {count: <error_hours>, period: hour}
        filter: _loaded_at >= current_date - <lookback_days>
  ```
  Run `dbt source freshness` before `dbt build`.
- Golden source tests: expected columns (light contract), PK uniqueness/not null or surrogate, completeness of dates/partitions, relationships, volume anomaly (packages such as dbt-expectations or Elementary).
- Singular tests in `tests/` return failing rows; name them `assert_<rule>`.
- Unit tests (`unit_tests:` in YAML, dbt >= 1.8) protect transformation logic with fixed inputs; use them for tricky CASE/date logic, not for every column.
- `--store-failures` keeps failing rows for diagnosis.
- In CI: `dbt build --select state:modified+`; publish only if no `error` test failed.
