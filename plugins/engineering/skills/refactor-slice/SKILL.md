---
name: refactor-slice
description: "Use after a slice works and before the merge, or on a periodic review of the project: tidy the code structure without changing behavior, guided by metrics."
---

# Refactor the slice

Objective: make the code right after it works, without changing what it does.

## Invariant rules

- Start only when every test is green. Finish with every test green.
- Pin the behavior with tests before touching the structure.
- Let metrics guide it (complexity, duplication, mutants, file size), not taste.
- Record the metrics before and after, for the system owner.
- A large structural change is not tidying. It becomes its own slice on the overall plan.

## Routes

| If | Read |
|---|---|
| the pass before merge (limits and actions) | `references/metrics.md` |
| the periodic review of the project's architecture | `references/architecture-review.md` |
