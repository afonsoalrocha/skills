---
name: aws-quicksight
description: Inspect, export, edit and test AWS QuickSight dashboards, analyses, datasets and data sources with AWS CLI v2 or boto3: list/describe, export definitions, publish versions, trigger and follow SPICE refreshes. Read-only by default. Not for validating the numbers themselves (dashboard-validation).
---

# AWS QuickSight

## Rules that always apply

- Access order: (1) AWS CLI v2 `aws quicksight ...`; (2) boto3 for automation or when
  responses must be processed as objects; (3) direct REST only if neither covers the case.
- Account, profile and region come from environment variables, never hard-coded:
  `AWS_PROFILE` (or `--profile`), `QUICKSIGHT_ACCOUNT_ID`, `AWS_REGION`. No static access
  keys in files; prefer SSO profiles.
- Authentication: if the SSO session expired, run `aws sso login --profile "$AWS_PROFILE"`,
  then confirm with `aws sts get-caller-identity`. Ask the user only when login needs
  interaction or fails. Do not loop logins and do not switch to another profile.
- `AccessDeniedException` is a missing permission, not an expired login: record the
  action that was denied and stop until the policy changes.
- Read-only by default. Any `create-*`, `update-*`, `delete-*` or permission change needs
  explicit approval from the user and a record in the asset's changelog
  (skill `bi-assets-as-code` when assets are versioned).
- List calls are paginated: follow `NextToken` (or a boto3 paginator) and check the total.
  A partial list is not "the asset does not exist".
- Exported definitions and data snapshots go to the request's data folder in external
  storage unless the asset is versioned as code.
- A dashboard visual is not the source of truth; to check its numbers use
  `dashboard-validation`.

## Vocabulary

Numbers reach a reader through dashboard → analysis → dataset → data source; a dataset in
SPICE is a copy refreshed by ingestions, so its freshness is the last successful one.
Full definitions: https://docs.aws.amazon.com/quicksight/latest/user/welcome.html

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| CLI commands: list, describe, export definition, publish a version, SPICE refresh | `references/cli.md` |
| Python with boto3: session, pagination, export, waiting on a refresh | `references/boto3.md` |
