---
name: databricks-workspace
description: "Use when querying Databricks (Spark SQL / Databricks SQL, Unity Catalog metadata) or moving files, notebooks and jobs between a local project and a Databricks workspace via the CLI or a SQL client."
---

# Databricks workspace

## Access order

1. **CLI** (`databricks`) for workspace files, jobs, clusters and warehouses.
2. **Project SQL client** (a thin module over the SQL Statement API or `databricks-sql-connector`) for queries and extraction.
3. **REST API directly** only when neither covers the case. Avoid heavy SDK layers for simple calls.

## Invariants

- Dialect is Spark SQL / Databricks SQL on Delta; never MySQL/Postgres syntax.
- Always fully qualify names: `<catalog>.<schema>.<table>`.
- Apply skill `sql-performance` before any SQL and `python-data-scripts` before any Python.
- Metadata first (catalog -> schema -> table -> columns); it is free and reads no data.
- Pass the SQL warehouse id explicitly from configuration (`DATABRICKS_WAREHOUSE_ID`); use the warehouse meant for analysis, not one reserved for other workloads.
- Inline results from the Statement API can be truncated silently: assert the expected row count.
- A shared sandbox schema is scratch space: fully qualified names, never a canonical source, never the final layer for dashboards.
- Credentials from environment (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`) or a CLI profile in `~/.databrickscfg`; never hard-coded, never printed.
- A local timeout does not cancel the statement: cancel it explicitly.
- Save extracts with the request (Parquet for intermediate, CSV only for small deliverables).

## Query flow

```python
# 1. metadata (no data read)
list_catalogs(); list_schemas("<catalog>"); list_tables("<catalog>", "<schema>")
get_table_info("<catalog>", "<schema>", "<table>")
# 2. query, warehouse id from config
df = execute_sql("SELECT ... FROM <catalog>.<schema>.<table> WHERE ...",
                 warehouse_id=os.environ["DATABRICKS_WAREHOUSE_ID"])
```

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| CLI commands, importing/exporting files and notebooks, syncing a project folder | `references/cli-workspace.md` |
| Large result: inline limit, keyset paging, checkpoint | skill `sql-performance`, keyset extraction |
| Profiling a huge partitioned table | skill `sql-performance`, large-table profiling |
| Reading a Spark plan / query profile | skill `sql-performance`, explain by engine |

Docs: https://docs.databricks.com/api/workspace/introduction ,
https://docs.databricks.com/en/dev-tools/cli/index.html
