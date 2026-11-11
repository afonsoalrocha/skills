---
name: review-delivery
description: "Use before merging a slice into the project or handing it to the system owner: automated checks, a fresh-context agent review, a reading of the diff, and a report in system language."
---

# Review the delivery

Objective: prove that the slice is right, and hand the system owner something they can sign without reading code.

## Invariant rules

- The order is: automated checks, an agent review with a fresh context, the engineer reading the diff, the owner's evaluation.
- A red check blocks. Never disable a check to make it pass.
- The engineer reads the diff, with attention on interfaces, schema, security, and changes that cannot be reversed.
- The owner evaluates behavior: acceptance tests, metrics, real use. Only humans sign.
- Evidence over narrative. Do not trust the agent's summary.

## Routes

| If | Read |
|---|---|
| setting up or checking pre-commit and CI | `references/automated-checks.md` |
| running the review with another agent | `references/agent-review.md` |
| reporting to the system owner | `references/owner-report.md` |
