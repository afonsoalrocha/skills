# Request README template

Copy into `requests/NNN-short-slug/README.md`. Every heading is filled before the status
moves to `in_build`. Write for a reader outside the data team.

```markdown
# NNN — Title

## Question
One paragraph. The question as the requester would recognise it.

## Requester and owner
Requester role (and person, if the project allows names). Owner of the analysis.

## Decision this supports
What will be done differently depending on the answer. If nothing changes, say so: the
request may be a quick check instead.

## Metrics
One line per metric: link to its card and its status (`certified`, `indicative`,
`blocked`). A blocked metric is listed with the question it cannot answer.

## Grain
The row the answer is allowed to have (for example: one row per month and segment).

## Period
The window, the time zone, and the rule for open or incomplete periods.

## Sources
Each source, the layer read, and what it is the source of truth for.

## Out of scope
What this request will not answer.

## Acceptance criteria
Block (the request cannot close while any fails):
- ...
Warn (the human reads and accepts or rejects):
- ...

## Results
Filled during the work: what was found, with period, filters, unit and data freshness.

## Validation
Checks that ran, their result, and anything left unverified.

## Status
Mirror of the registry: current status and the date of the last transition.
```

## Writing good acceptance criteria

- Each criterion can be checked by a script or by a named person. "Numbers look right" is
  not a criterion.
- State tolerance explicitly when comparing totals (absolute or relative, and against what).
- Separate block from warn. A block protects correctness; a warn asks for human judgment.
- Thresholds come from the requester or the metric owner, never from what the data shows.

## Engineering requests

Keep the same headings. "Metrics" becomes the measurable outcome (for example latency,
freshness or cost, each with its definition), "Grain" may be "n/a", and acceptance criteria
name the tests or checks that must pass.
