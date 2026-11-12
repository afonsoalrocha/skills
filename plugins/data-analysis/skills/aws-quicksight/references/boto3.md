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

## API pitfalls

- After every mutation, read the resource back and confirm the effect; a successful response is not proof.
- Permission updates on dashboards, datasets, topics and apps usually replace the whole set, not a delta: read the current state and send the final set, or use the grant/revoke calls, so nothing is dropped. Compare permission sets as sets (principal and action), never by response order.
- Updating a Topic can drop configuration the call did not resend, such as its refresh schedule: re-describe the schedule afterwards and restore it if missing.
- A local SDK can lag the service and lack a newer operation: upgrade it or load the current service model before concluding the API cannot do it.

Docs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html
