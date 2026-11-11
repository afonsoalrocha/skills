---
name: design-architecture
description: "Use when deciding the structure of an application or module: domain, glossary, decisions (ADRs), deep modules, stack, and robustness against failures."
---

# Design the architecture

Objective: a structure that is simple, testable, and reversible for what the next slice needs.

## Invariant rules

- A modular monolith of deep modules: a small interface, with a lot of behavior behind it.
- Business rules live in pure functions at the center. The database, the network, and the interface sit at the edges. Dependencies point inward.
- Validate data where it enters. Use types that make invalid states impossible.
- Keep the stack simple and cheap until a measurement shows that something is missing.
- Limits: CRAP below about 10 per function, and files under 500 lines.
- Do not design for future slices. Build only what the next one asks for, and do not close doors.

## Routes

| If | Read |
|---|---|
| naming a concept or recording a hard decision | `references/glossary-and-adrs.md` |
| defining modules, interfaces, and where each rule lives | `references/deep-modules.md` |
| choosing a stack, database, queue, or infrastructure | `references/simple-stack.md` |
| there is external I/O, jobs, payments, or concurrency | `references/robustness.md` |
