# Writing the validator

- Collect all failures; do not stop at the first one.
- Print one ASCII line per check: `OK`, `ERROR` or `WARN`, then the check name and detail.
- Exit non-zero when any `ERROR` exists, so shells and CI can gate on it.
- Use explicit checks, not bare `assert` (removed under `python -O`).
- Parameters (key, window, expected count, tolerance) come from the contract or CLI args,
  never hard-coded inside the check functions.
- For transform functions, test with `pytest` and fixtures stored in **files**; inline
  JSON or backslashes in a shell command get mangled.
- Keep the validator next to the script it validates and give it the same number
  (`02_extract.py` -> `02_validate_extract.py`).

Template: `scripts/validator_template.py` (copy, rename, fill the contract).
