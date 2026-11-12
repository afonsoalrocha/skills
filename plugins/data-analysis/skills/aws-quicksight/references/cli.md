# AWS CLI v2 for QuickSight

All commands assume `AWS_PROFILE`, `AWS_REGION` and `QUICKSIGHT_ACCOUNT_ID` are set.
`A="--aws-account-id $QUICKSIGHT_ACCOUNT_ID"` keeps lines short.

| Operation | Command |
|-----------|---------|
| List dashboards | `aws quicksight list-dashboards $A` |
| Describe dashboard | `aws quicksight describe-dashboard $A --dashboard-id ID` |
| Export dashboard definition | `aws quicksight describe-dashboard-definition $A --dashboard-id ID` |
| List / describe analyses | `list-analyses $A` / `describe-analysis $A --analysis-id ID` |
| Export analysis definition | `describe-analysis-definition $A --analysis-id ID` |
| List / describe datasets | `list-data-sets $A` / `describe-data-set $A --data-set-id ID` |
| List / describe data sources | `list-data-sources $A` / `describe-data-source $A --data-source-id ID` |
| Dashboard permissions | `describe-dashboard-permissions $A --dashboard-id ID` |
| Update a dashboard (approval) | `update-dashboard $A --dashboard-id ID --name ... --definition file://def.json` |
| Publish a version (approval) | `update-dashboard-published-version $A --dashboard-id ID --version-number N` |
| Start SPICE refresh (approval) | `create-ingestion $A --data-set-id ID --ingestion-id refresh-$(date +%Y%m%d%H%M%S)` |
| Refresh status | `describe-ingestion $A --data-set-id ID --ingestion-id ING` |
| Refresh history | `list-ingestions $A --data-set-id ID` |

## Examples

```bash
# All dashboards, every page (the CLI paginates automatically unless --no-paginate)
aws quicksight list-dashboards $A --query 'DashboardSummaryList[].[DashboardId,Name]' --output table

# Export a definition for review or migration
aws quicksight describe-dashboard-definition $A --dashboard-id "$DASH_ID" \
  --output json > "$REQUEST_DATA_DIR/dashboard-definition.json"

# Find the datasets behind a dashboard
aws quicksight describe-dashboard $A --dashboard-id "$DASH_ID" \
  --query 'Dashboard.Version.DataSetArns'

# Read the custom SQL of a dataset (to reproduce its numbers)
aws quicksight describe-data-set $A --data-set-id "$DS_ID" \
  --query 'DataSet.PhysicalTableMap.*.CustomSql.SqlQuery'
```

After an update, publish explicitly and confirm the published version number. After a
refresh, poll `describe-ingestion` until `COMPLETED` or `FAILED` and report the row counts
and errors it returns.

## Documentation

- API reference: https://docs.aws.amazon.com/quicksight/latest/APIReference/
- CLI reference: https://docs.aws.amazon.com/cli/latest/reference/quicksight/
