---
name: close-request
description: "Close a formal request (analytics or engineering) only after explicit human approval: run its gates, label the outcome complete/partial/blocked, write the insight log, do the knowledge review and record the closed transition. Not for opening or moving a request (new-request)."
---

# Close a request

## Rules that always apply

- **Only the human closes.** Never close on your own, because work looks finished, or
  because a request has been idle. Ask, and wait for an explicit yes.
- The close outcome is separate from the lifecycle status:
  - `complete`: every block criterion passed; warnings, if any, were read and accepted.
  - `partial`: closes only after the human writes the accepted gap in the transition reason.
  - `blocked`: does not close. The request stays open (or `paused`) with the reason.
- Every block criterion from the README ran on the final result. A request whose gates
  were not run is not closed.
- Warnings are shown to the human. Never delete or silence a warning to make a report clean.
- A `paused` request cannot carry an outcome: resume it first.
- The insight log and the revision log are append-only.

## Steps

1. Re-read the README acceptance criteria. Run every check they name, on the final outputs.
2. Label the outcome (`complete` / `partial` / `blocked`) with the checks that passed and failed.
3. Write or update `insights.md` in the request folder (template: `references/insight-log.md`).
4. Do the knowledge review (`references/knowledge-review.md`) and list in the README which
   articles or metric cards changed, or why nothing did.
5. Show the human: outcome, failed/warned checks, insights, knowledge changes. Ask to close.
6. After the explicit yes:
   `python <skills-dir>/new-request/scripts/registry.py close NNN <complete|partial> "<reason>"`
   then the same script with `validate`.
7. Fill the closing fields in the README: closed on, result, impact, follow-ups created,
   final scripts. If there is an external ticket, move it and link the published docs.
8. Merge the request branch following the project's git workflow.

Registry fields and allowed transitions are in the `new-request` skill, reference `registry.md`.

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| Writing `insights.md` (recommendation, findings, append-only revision log) | `references/insight-log.md` |
| Knowledge review: what deserves to be recorded and where | `references/knowledge-review.md` |
| Registry fields and transitions | the `new-request` skill, reference `registry.md` |

Closing a request does not retire a data product it created; the product has its own changelog.
