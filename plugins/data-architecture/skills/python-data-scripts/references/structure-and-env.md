# Structure, imports, config, logging, tests

## Structure
- Separate extract -> validate -> transform -> deliver, as functions or numbered scripts (`01_extract.py`, `02_validate_extract.py`, ...).
- Promote reusable code to a shared package. A deliverable script longer than the project's size budget (default: 500 lines, overridable in project config) is a signal to split.
- Do not mix query, business rule and file writing in one block; no global state; no mutable default args (`def f(x=[])`).
- Shared functions get type hints and a one-line docstring. Business constants (tenant IDs, windows) come from args or config.

## Imports
- Make the project an editable package (`pyproject.toml`, `pip install -e .`) and import `from <package>.connectors.<engine> import ...` from anywhere.
- `ModuleNotFoundError: <package>` usually means the venv lost the editable install: reinstall.
- Migrate legacy `sys.path.insert` only in scripts you are already changing.

## Config and secrets
- Read environment variables or `.env` (`python-dotenv`) at the edge; parameterize with `argparse` (window, source, `--dry-run`).
- Read an external CSV that may carry a BOM with `encoding="utf-8-sig"`; otherwise the first column becomes `\ufeffname` and the join key never matches.
- Check which variable names exist with a script that prints names only, never values.

## Logging and subprocess
- Recurring jobs: `logging` with level and timestamp. One-off checks: ASCII `print` is enough.
- `subprocess.run([...], check=True, timeout=...)`; never `shell=True` with interpolated text.

## Tests
- `pytest` on pure transform functions with fixtures in files.
- No test queries production.
