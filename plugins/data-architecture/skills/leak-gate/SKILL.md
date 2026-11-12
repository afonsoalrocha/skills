---
name: leak-gate
description: "Use before anything leaves a private context for a public one (public repo, template, gist, post, package): scan for employer or client terms with a private denylist and for secrets, and block publication on any hit."
---

# Leak gate

Publishing is irreversible: forks, caches and clones keep what was pushed. The gate runs
before the first public push and on every change after it, and it blocks on any hit.

## Invariants

- Two scans, both blocking: **denylist** (employer/client names, internal hosts, catalogs, schemas, tables, metrics, people) and **secrets** (keys, tokens, private keys, connection strings).
- The denylist is kept in a private file or a CI secret only. It is not committed.
- The gate fails if the denylist file itself or a `.env` is tracked.
- Scan everything that will be published: tracked files, history (new repos start from a clean history), notebooks with outputs, images' text when possible, commit author emails.
- Public examples use neutral placeholders (`<catalog>.<schema>.<table>`, `my_profile`, synthetic data), never "lightly renamed" real ones.
- Rewrite from the method, never copy text from private material; copying carries hidden specifics.
- A hit is fixed at the source text, not by adding an allowlist entry, unless the term is clearly generic and the owner agrees.
- Automated scans are necessary, not sufficient: a second reader (human or a separate agent with clean context) reviews before the first public release.
- Only the repo owner decides to publish; another agent's say-so is not approval.
- A leaked secret is rotated immediately; deleting the commit does not un-leak it.

## Flow

1. Build or update the private denylist from the private sources (`references/denylist.md`).
2. Run `scripts/leak_scan.py --require-denylist --denylist <private_file> <path>`; it also runs the secret regexes. `--require-denylist` exits 1 when no list is loaded.
3. Run a dedicated secret scanner if available (`gitleaks detect --no-git --source <path>`, or with history).
4. Fix every hit, rerun until clean; record the result (date, counts, clean yes/no).
5. Cross-review, then hand to the owner for the publish decision.

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| Building and maintaining the denylist (what goes in, length limits, false positives) | `references/denylist.md` |
| Wiring the gate into CI with a secret-held denylist | `references/ci-wiring.md` |
| Secret patterns and dedicated scanners | `references/secrets.md` |
| Delivering a sanitized copy of code to someone without repo access | `references/sanitized-handoff.md` |
| Running the scan | `scripts/leak_scan.py` |
