# Databricks CLI and workspace sync

Authenticate once (`databricks auth login --host <workspace-url>` or a profile in
`~/.databrickscfg`); select with `--profile my_profile` when you have several.

| Operation | Command |
|-----------|---------|
| List a folder | `databricks workspace list <remote_dir>` |
| Import a plain file (module, HTML, CSV, SVG) | `databricks workspace import <remote_path> --file <local_path> --format RAW --overwrite` |
| Import a Python notebook | `databricks workspace import <remote_path_without_ext> --file <local.py> --format SOURCE --language PYTHON --overwrite` |
| Export | `databricks workspace export <remote_path> --file <local_path>` |
| Sync a folder (incremental) | `databricks sync <local_dir> <remote_dir>` |
| Clusters / jobs / warehouses | `databricks clusters list`, `databricks jobs list`, `databricks warehouses list` |

## Import rules
- A notebook is a `.py` whose first line is `# Databricks notebook source`: use `--format SOURCE --language PYTHON`, and drop the `.py` from the remote path.
- Everything else uses `--format RAW`.
- `--overwrite` updates existing files; check you are in the right remote folder first.
- Remote user folder pattern: `/Users/<user-email>/<project>/`; keep the email in config, not in docs or code.
- For anything beyond ad-hoc sync, prefer Databricks Asset Bundles (`databricks bundle deploy`) so jobs and code are versioned together.
