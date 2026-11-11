# Code and tests

## Functions and modules
- Small enough to understand and change in isolation. Review signals (defaults, overridable in project config: 30 lines, 4 parameters, 3 nesting levels) are signals, not violations.
- Extract only for real gains in cohesion, clarity, reuse or testability.
- Names reveal intent and are searchable; side effects are obvious from the name or docstring.

## Types, comments, data
- Type hints on public interfaces; dataclasses for data models when they add clarity.
- Comments keep the why, provenance, business rule or external constraint, not obvious syntax. Agents read these too.
- Errors carry enough context to diagnose, never secrets.

## Duplication
- Remove duplication of the same business rule; avoid premature abstraction of look-alikes.
- Follow existing patterns unless they cause errors or duplication.

## Risk-based tests
- Test business rules, filters, ordering, totals, classifications, paging, fallbacks, links and model-to-artifact transforms.
- Every bug fixed in a deterministic rule gets a regression test when feasible.
- No chasing coverage or testing library internals.
- Each job offers a validation command and, when it renders artifacts, a smoke test on small local data.
- Tests never query production; fixtures live in files.
