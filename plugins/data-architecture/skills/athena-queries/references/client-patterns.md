# Client patterns (boto3)

```python
import boto3, time
session = boto3.Session(profile_name=os.environ.get("AWS_PROFILE", "my_profile"))
athena = session.client("athena")

qid = athena.start_query_execution(
    QueryString=sql,
    QueryExecutionContext={"Catalog": "<catalog>", "Database": "<database>"},
    WorkGroup=os.environ["ATHENA_WORKGROUP"],
)["QueryExecutionId"]

deadline = time.monotonic() + timeout_s
while True:
    q = athena.get_query_execution(QueryExecutionId=qid)["QueryExecution"]
    state = q["Status"]["State"]
    if state in {"SUCCEEDED", "FAILED", "CANCELLED"}:
        break
    if time.monotonic() > deadline:
        athena.stop_query_execution(QueryExecutionId=qid)   # timeout cancels
        raise TimeoutError(qid)
    time.sleep(1)
stats = q["Statistics"]  # DataScannedInBytes, EngineExecutionTimeInMillis
```

- Page results with the `get_query_results` paginator; the first row of the first page is the header.
- Every value is a string or missing: build a dtype map from `ResultSetMetadata.ColumnInfo` and cast explicitly (`decimal` -> `Decimal`, `date` -> date, IDs stay `str`).
- Metadata: `list_data_catalogs`, `list_databases`, `list_table_metadata` (paginated), `get_table_metadata` returns `Columns` and `PartitionKeys`.
- On `AccessDeniedException`, log the action and resource ARN and stop.
