---
name: quick-check
description: Answer a small, ad hoc data question fast while leaving a reproducible trail (a dated folder with notes and the query). Use when someone wants a number or a sanity look without a decision or acceptance criteria behind it. Formal work goes to new-request; scheduled work is a pipeline.
---

# Quick check

A quick check trades ceremony for speed, but never for traceability: anyone should be able
to rerun it next month and get the same answer for the same cut. If the question has a
decision and acceptance criteria behind it, it is not a quick check.

## Setup

`python scripts/quick_check.py new <slug>` (paths relative to this skill; run from the
project root) creates `quick-checks/<today>-<slug>/` with a notes README and `scripts/`.
Template of the notes: `references/readme-template.md`.

## While working

- Keep every query and helper in the check's `scripts/` as files run by path; inline shell
  snippets are for one-liners only.
- Reuse an extract already on disk when cut and data are unchanged.
- Extracts and heavy outputs live in external storage; the repo gets notes and code only.
  Ephemeral files use the OS temp directory and are cleaned up; no `tmp/` in the repo.
- Secrets and personal data never reach git; refer to environment variables by name.
- The answer is a reading, not a publication: a metric that has a card keeps the card's
  status label, and nothing gets certified here.
- Before writing the conclusion, apply the quick-check minimum of `data-integrity-tdd`
  (grain, count against source, time window) and note the outcome.

## States

| State | How it gets there |
|-------|-------------------|
| `open` | set on creation |
| `closed (date)` | `quick_check.py close-stale` at session start closes checks created on earlier days |
| stays `open` | the README has a `Keep open:` line (only on the user's request) or a `HANDOFF.md`; remove the line once the pending item is done |
| `open` again | `quick_check.py reopen <folder>` |

"Close it", said by the user, also means: commit that folder alone (notes and code, no
data) through the project's git workflow.

## When it outgrows itself

| Signal | Move to |
|--------|---------|
| A decision now depends on it, with criteria | `new-request`, linking this check |
| Others reuse the logic | the project's shared scripts |
| It is asked on a schedule | a recurring pipeline |

`python scripts/quick_check.py --help` lists every command.

## Routes

| If | Read |
|---|---|
| writing the notes for a check | `references/readme-template.md` |
