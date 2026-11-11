---
name: ship-to-production
description: "Use when deploying, changing the production database, configuring logs and alerts, or deciding whether and how to scale an application."
---

# Ship to production

Objective: reach production in steps that are small, frequent, and reversible, and see what is happening there.

## Invariant rules

- Deploy only with green CI and a known rollback.
- Put new behavior behind a feature flag when there is risk.
- More rigor, and a human review, for money, data, migrations, and public libraries.
- Structured logs and alerts from the first slice.
- Scale only after measuring the bottleneck.

## Routes

| If | Read |
|---|---|
| making or preparing a deploy | `references/reversible-deploy.md` |
| changing schema or data in production | `references/migrations.md` |
| configuring logs, metrics, and alerts | `references/observability.md` |
| deciding whether and how to scale | `references/when-to-scale.md` |
