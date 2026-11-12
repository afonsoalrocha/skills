# `insights.md`

One per request, in the request folder. It is what a reader opens first after the
request closes.

```markdown
# Insights — request NNN

## Recommendation
The action a reader can take, in one or two sentences.

## Context
Question, data used, period, filters, and the limits of both data and method.

## Findings
Each finding with its number, unit, period and source. Mark each one as:
- validated fact (passed the checks),
- inference (reasoned, not directly measured), or
- open (needs more data or a decision).

## Recommendations
Concrete next steps, each with an owner role.

## Files
Final scripts and outputs (outputs by link to external storage, never a local disk path).

## Revision log
Append-only. Add a dated entry; never rewrite an earlier one.

### YYYY-MM-DD — Title
What changed in the reading, and what was left as it was.
```

Rules:
- Indicative metrics carry their indicative label wherever they appear. Blocked metrics
  appear only as the question that could not be answered, and why.
- A number without period and source is not a finding.
- Absence of data is reported as unavailable, never as zero.
