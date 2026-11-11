# Secrets

- Built-in regexes in `scripts/leak_scan.py` cover: AWS access key IDs, GitHub/GitLab tokens, Slack tokens, Google API keys, private key blocks, JWT-like strings, generic `password=`/`token=`/`secret=` assignments with literal values, URLs with embedded credentials.
- Prefer a dedicated scanner on top: gitleaks (`gitleaks detect --source . --no-git` for a folder, without `--no-git` for history) or trufflehog.
- Placeholders that look like secrets (`<token>`, `my_token`, `xxxx`) are fine; real-looking random strings in examples are not.
- A real secret found: rotate first, then clean history, then report.
