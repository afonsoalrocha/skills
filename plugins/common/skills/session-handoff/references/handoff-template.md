# `HANDOFF.md` template

The script writes this layout. Fill the arguments so each section answers one question.

| Section (argument) | Answers | Holds | Does not hold |
|--------------------|---------|-------|---------------|
| Goal (`--goal`) | What is this work for? | One sentence | Background, history |
| Done (`--done`) | What exists now? | Script path, file name, count, check result | Result rows, pasted code |
| Decisions (`--decision`) | What was chosen, and why? | Choice plus the reason | Rules that outlive the task |
| Pending (`--pending`) | What blocks or is open? | Blocker, open question, who can answer | Wishes |
| Next step (`--next`) | What does the next session do first? | One concrete action | A plan of five steps |
| Cache (`--cache`) | Where are data and outputs? | Folder paths in external storage | Data itself |

State (`--state`): `in_progress` (default), `in_review` (waiting for the human to review),
`blocked`. Never `done`.

## Filled example

```markdown
# Handoff - 042-order-lag

- Updated: 2025-01-15 17:40 +0000
- From: agent-a | To: agent-b
- State: in_progress (never 'done' without the user's explicit approval)
- Git: feature-order-lag; 3 changed file(s) in this folder

## Goal
Measure the delay between order creation and payment confirmation per channel.

## Done (with evidence: script, file or number)
- scripts/extract_orders.py runs clean; data/orders.parquet has 120,431 rows
- scripts/check_integrity.py passes 4 of 4 checks on that file

## Decisions
- Period is the last full 90 days: older rows use another status model

## Pending and blockers
- Channel "unknown" is 6% of rows; needs an owner to say what it is

## Next step
Run scripts/lag_by_channel.py on data/orders.parquet and compare with the totals in the README.

## Cache and outputs
- <external-storage>/requests/042-order-lag/data/
```

## Rules for the text

- Numbers carry a unit and a period. Absence of data is "unavailable", never zero.
- A decision without its reason is not a decision; leave it out.
- If the handoff grows past the limit, it is holding too much: move detail to the README
  or a script and keep the pointer.
