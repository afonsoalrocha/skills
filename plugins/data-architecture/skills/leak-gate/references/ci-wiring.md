# CI wiring

- Store the denylist as a repository secret (e.g. `LEAK_DENYLIST`, multiline).
- In the job: write the secret to a gitignored path, run the scan, delete the file in an `always()` step.
- With no secret configured, the content scan is a no-op that says so loudly; the tracked-file checks still run. Do not report "clean" when the denylist was missing. `--require-denylist` exits 1 when no terms are loaded.
- Never echo the denylist or print matched lines with surrounding context in public CI logs; print file path and a term index or hash instead.
- Run the secret scan (gitleaks action or CLI) in the same workflow, on full history for the first release.
- Make the job required on the default branch.

```yaml
- name: Leak gate
  env:
    LEAK_DENYLIST: ${{ secrets.LEAK_DENYLIST }}
  run: |
    if [ -n "$LEAK_DENYLIST" ]; then printf '%s\n' "$LEAK_DENYLIST" > .leak-denylist.txt; fi
    python scripts/leak_scan.py --require-denylist --denylist .leak-denylist.txt --hide-terms .
- name: Clean up
  if: always()
  run: rm -f .leak-denylist.txt
```
