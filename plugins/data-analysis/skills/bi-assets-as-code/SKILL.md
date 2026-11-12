---
name: bi-assets-as-code
description: "Version published BI assets (dashboards, datasets, semantic models, workspaces, apps) as code under products/: asset.yaml, CHANGELOG, unique resource ids, declared relationships, reproducible publishing. Any BI tool. Not for data contracts or pipeline models (data engineering)."
---

# BI assets as code

Each published BI asset is a small data product with its own folder, manifest and history,
so its published state can be rebuilt from git and every change is traceable.

## Rules that always apply

- One folder per asset: `products/<type>/<asset-id>/` with `asset.yaml`, `CHANGELOG.md`,
  and the scripts or definitions that publish it. Types are folders (`dashboards/`,
  `datasets/`, `workspaces/`, `apps/`...); assets never nest inside each other.
- `resource_id` (the id in the BI tool) is unique across **all** asset types in the project.
- Relationships are declared in `asset.yaml`; every relationship has its inverse in the
  other asset's manifest. A container (workspace, space, folder) holds only structure,
  membership and permissions; it does not own the assets it groups.
- **Before changing**: read the README, the changelog, the current scripts and evidence.
  **After**: append to `CHANGELOG.md` (date, asset, why, change, validation, result).
  Never delete history; mark superseded artifacts as such.
- The published state must be reproducible from versioned scripts. A manual change in the
  tool is recorded with how to reproduce it, or redone by script.
- **Before creating a dataset**, list existing datasets on the same source and extend one
  additively (new columns at the end, regression check that old columns did not change)
  instead of opening a parallel copy. A new dataset needs a stated reason.
- Sharing a container does not grant access to the assets inside it: grant and verify
  access on each asset. Permission changes need explicit approval.
- Column or metric changes on an asset update the metric card or knowledge article in the
  same piece of work (`metric-card`, `knowledge-base`).
- A request that created the asset is never closed without explicit approval; closing it
  does not retire the asset.

## Validate in proportion to the change

| Asset type | Validate |
|------------|----------|
| Dataset | schema, row count after refresh, regression of existing columns |
| Dashboard | numbers on key visuals (`dashboard-validation`), filters, published version |
| Natural-language or Q&A layer | indexing done, a fixed set of acceptance questions answered correctly |
| Permissions | effective access of a sample user, not only the API response |

`python scripts/validate_assets.py` (paths relative to this skill) checks manifests:
unique ids, inverse relationships, changelog present.

## Routes

| If the task is... | Read |
|-------------------|------|
| `asset.yaml` fields and a changelog entry | `references/manifest.md` |
| Tool-specific commands | the tool's skill (for example `aws-quicksight`) |
