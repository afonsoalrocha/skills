---
name: implement-slice
description: "Use when writing code with an AI agent for a slice that already has a spec, or when fixing a bug: test first, smallest change, small commits, one agent per task."
---

# Implement a slice

Objective: make the slice's acceptance tests pass, in small steps that have been proven.

## Invariant rules

- One agent, one task per session. When the context has swollen, hand off or compact.
- A test first, failing for the expected reason, at the agreed test point. Then the smallest change that passes.
- While implementing, only make it pass. The tidying comes in `refactor-slice`, before the merge.
- Keep a comment when it is useful. It explains why, and the origin (a bug, an issue, an external constraint), never the obvious.
- Small commits that say why, what changed, and how it was proven.
- A bug is fixed only after it has been reproduced, with a regression test written before the fix.
- Robustness (timeouts, retry, idempotency, locks) is requested explicitly. See `design-architecture`.

## Routes

| If | Read |
|---|---|
| the test and implementation cycle, and the testing rules | `references/tdd-cycle.md` |
| fixing a bug | `references/fix-bug.md` |
| creating or updating the repository AGENTS.md | `references/agents-md.md` |
| the module touches money, data, or a critical rule | `references/mutation-testing.md` |
