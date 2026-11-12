# Gate results and metric status

Status and definition live in the `metric-card` skill (data-analysis plugin). Do not
restate the formula, grain, owner, filters or maturity here, and do not invent a
parallel lifecycle. The agreed statuses are `certified`, `indicative` and `blocked`.

This skill only maps a gate result onto that status for a given run:

- A failed `block` gate means the metric is not published as `certified` that run.
- A `warn` gate does not, by itself, change the card; record it next to the result.
- A `block` failure never fails silently: the run reports the failed gate, and
  publication of a certified figure is withheld until the gate passes or the card
  owner changes the status.

Severity changes and gate removals still follow the invariants in `SKILL.md`.
