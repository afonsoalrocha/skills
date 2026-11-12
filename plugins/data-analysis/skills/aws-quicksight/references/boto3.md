# boto3 for QuickSight

Use when results feed other scripts. Same profile as the CLI; no static keys.

```python
import os
import time

import boto3

session = boto3.Session(profile_name=os.environ.get("AWS_PROFILE"))
qs = session.client("quicksight", region_name=os.environ["AWS_REGION"])
account = os.environ["QUICKSIGHT_ACCOUNT_ID"]

# Paginate: never trust the first page
dashboards = []
for page in qs.get_paginator("list_dashboards").paginate(AwsAccountId=account):
    dashboards.extend(page["DashboardSummaryList"])
print(len(dashboards), "dashboards")

# Export a definition to a file, failing loudly
import json
from pathlib import Path

from botocore.exceptions import ClientError


def export_definition(dashboard_id: str, target: Path) -> Path:
    try:
        resp = qs.describe_dashboard_definition(AwsAccountId=account, DashboardId=dashboard_id)
    except ClientError as err:
        code = err.response["Error"]["Code"]
        if code == "AccessDeniedException":
            raise SystemExit(f"denied: DescribeDashboardDefinition on {dashboard_id}") from err
        if code == "ResourceNotFoundException":
            raise SystemExit(f"dashboard {dashboard_id} not found in {account}") from err
        raise
    payload = {"DashboardId": dashboard_id, "Name": resp.get("Name"),
               "Definition": resp["Definition"]}
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix(target.suffix + ".partial")
    partial.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    partial.replace(target)  # no half-written file on failure
    return target

# Follow a refresh that was started with approval
def wait_ingestion(dataset_id: str, ingestion_id: str, every: int = 15) -> dict:
    while True:
        ing = qs.describe_ingestion(AwsAccountId=account, DataSetId=dataset_id,
                                    IngestionId=ingestion_id)["Ingestion"]
        if ing["IngestionStatus"] in ("COMPLETED", "FAILED", "CANCELLED"):
            return ing
        time.sleep(every)
```

- Catch `botocore.exceptions.ClientError`; an `AccessDeniedException` code stops the script
  with the denied action in the message.
- Write outputs atomically (temp file then rename) to the request's data folder.
- Some APIs replace whole sets (for example permissions): read the current state first and
  send the full intended set, or use the grant/revoke fields, so nothing is dropped.

Docs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html
