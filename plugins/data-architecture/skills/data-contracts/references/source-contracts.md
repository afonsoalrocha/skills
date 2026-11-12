# Contracts on ingested sources

- You rarely control the source; the contract states what you expect and detects drift early.
- Light contract first: expected columns present, PK unique and not null, freshness threshold.
- Schema drift policy: new column -> warn and ignore until modeled; missing or retyped column -> block before staging builds.
- Check completeness of dates/partitions and volume bands at the source (skill `data-quality-gates`).
- Record the source version or snapshot compared when reporting a divergence.
- Agree a notification path with the source owner for planned breaking changes.
