# Ledger and reminder

The ledger is an append-only file kept with the project (for example `retrospective.md`).
Add one line per reviewed day, including days with no findings:

```
- YYYY-MM-DD - sessions N, relative cost X - findings: [label] summary; ... - proposals: 1 approved, 2 rejected (or "nothing to change")
```

The line must begin with `- ` and the ISO date: the reminder script finds reviewed days
by that shape.

## Rules

- **Append only.** When decisions arrive later, add a new line for the same day; do not
  edit the old one.
- **Short, stable mechanism labels** in brackets, such as `[shell-escaping]`,
  `[re-read]`, `[wrong-profile]`, so a plain text search shows recurrence. Reuse a label
  instead of inventing a near-duplicate.
- Keep names of customers and any secret out of the ledger.
- Commit the ledger together with the changes that were approved.

## Optional reminder at session start

`scripts/pending.py` lists past days that have sessions and no ledger line:

```
python <skills-dir>/session-retrospective/scripts/pending.py \
  --project-dir <transcripts folder> --ledger <ledger file> --since YYYY-MM-DD
```

Wire it to a session-start hook if the agent supports one. It prints at most one line,
always exits 0, and never blocks. On seeing the notice, offer the review to the human;
do not run it unasked. It depends on the same Claude Code transcript format as the
collector.
