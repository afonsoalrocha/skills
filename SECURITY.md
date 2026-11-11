# Security

This repository is public. Write every file as if a stranger will read it.

## Do not commit

- Company names, product names, or internal team names
- Table names, schema names, column names, or metric definitions from a real system
- Customer data, sample rows, or anything derived from them
- Business rules that belong to one organization
- Secrets: tokens, passwords, keys, connection strings, private URLs

Project-specific context stays in that project's `AGENTS.md` or `CLAUDE.md`. Those files point at the skills here. They are not copied into this repository.

## Checks on pull requests

`scripts/validate.sh` checks skill structure. When the repository secret `LEAK_DENYLIST` is set, the same script scans the tree for those terms, one per line. If the secret is absent or blank, the scan prints a notice and continues. A match fails the check. The log names the file and does not print the term.

The workflow also runs gitleaks, for credential shapes.

The maintainer creates `LEAK_DENYLIST` in the repository settings. Do not store the terms in the repository, in a workflow file, or in a pull request.
