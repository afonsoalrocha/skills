---
name: spec-next-slice
description: "Use before building something new or the next part of an application: a short interview, an overall plan in slices, and a short spec of only the next slice, with acceptance tests the system owner approves."
---

# Specify the next slice

Objective: leave with the next slice decided and its acceptance criteria approved, without specifying the future.

## Invariant rules

- Keep an overall plan of the whole, one line per slice. Detail **only the next slice**. Detail for later slices goes stale as soon as the current one is implemented.
- Keep the spec to about one page. If a sentence does not become a test, it probably does not belong.
- Acceptance criteria are tests in natural language, and the system owner approves them before any code.
- Agree the test points (the public interfaces) with the owner before implementing.
- Search the code, the documents, and memory before asking.

## Routes

| If | Read |
|---|---|
| conducting the interview with the owner | `references/interview.md` |
| creating or revising the project's overall plan | `references/overall-plan.md` |
| writing the slice spec | `references/spec-format.md` |
| writing the acceptance criteria | `references/acceptance-tests.md` |

Next: modeling and architecture in `design-architecture`; code in `implement-slice`.
