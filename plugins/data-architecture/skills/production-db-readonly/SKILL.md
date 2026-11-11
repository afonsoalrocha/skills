---
name: production-db-readonly
description: "Use when querying a production transactional database (MySQL or PostgreSQL) for deep validation, source-of-truth checks or data not yet in the lake. Read-only, through the project's connector, in the database's own dialect."
---

# Production databases, read-only

The transactional database is the last level of the validation hierarchy
(report -> mart -> staging -> source system). Go there when upper layers disagree or the
data has not landed in the lake yet. It serves live traffic: every query is a guest.

## Invariants

- Read-only. No `INSERT/UPDATE/DELETE/DDL`; the connector refuses non-read statements (`scripts/readonly_guard.py`), and the DB user should be read-only too: a first-verb check never replaces database grants.
- Prefer a read replica over the primary; know which one feeds the BI tool you are reconciling against.
- Connect only through the project's connector module; never ad-hoc drivers, never an MCP or GUI session for scripted work.
- Credentials from environment variables or a secret store; never in code, logs or notebooks; never print them.
- Write the query in the database's own dialect (route below), never Spark/Trino syntax.
- Apply skill `sql-performance` before every query: project, filter by indexed ranges, aggregate in the engine.
- `EXPLAIN` before any heavy read; `EXPLAIN ANALYZE` runs the query, so weigh production impact first.
- Set a statement timeout and bounded result size on every session.
- Replication lag is real: when replica and primary differ, record the instant compared.
- Save the query script with the request for reproducibility.

## Connector contract (what the project module should expose)

| Function | Purpose |
|----------|---------|
| `execute_sql(query, params, target)` | parameterized SELECT, returns a DataFrame |
| `list_databases(target)` / `list_schemas(...)` / `list_tables(...)` | discovery without scanning |
| `get_table_info(table, ...)` | columns, types, keys, comments |

`target` is an alias (e.g. `primary`, `replica`) resolved from configuration, never a host
literal in analysis code.

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| MySQL: dialect notes, EXPLAIN, session timeouts, metadata queries | `references/mysql.md` |
| PostgreSQL: dialect notes, EXPLAIN, `statement_timeout`, read-only transactions | `references/postgres.md` |
| Unstable connection (DNS, VPN, first attempt timeouts) | `references/connectivity.md` |
| Guarding a connector against write statements | `scripts/readonly_guard.py` |
