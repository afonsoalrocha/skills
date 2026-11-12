# Propose

Prefer the fix that is most deterministic: **script or function, then hook or permission,
then configuration, then test, then skill or rule text.** A written reminder is the last
resort.

Where the fix lives follows "Where an instruction lives" in `CONVENTIONS.md`. Two causes
need more than that table:

- A wrong analytical conclusion goes to the work's own README or insights and outputs. If
  it was already delivered, the proposal names who must be told. The notice is the
  human's.
- A personal preference about how to work goes to agent memory, not to a skill.

## Proposal format

Number items in sequence, continuing the ledger's numbering. Each one answers, in a few
lines:

1. **Symptom.** What happened, on which days and sessions (evidence from the summary).
2. **Probable cause.** And why you think so.
3. **Exact change.** The file, and the diff or the before/after text.
4. **How to validate.** How to know it fixed the problem without a regression.
5. **Saving.** How much it saves or which error it prevents, with a number only if the
   summary shows one.

## Priority

1. A wrong conclusion that was delivered.
2. Impact on data.
3. Stale knowledge.
4. Rework.
5. Tokens.

Present the ordered list and let the human decide item by item ("approve 3, reject 4").
The human may ask for an analysis to be reopened first; then redo the check at the source
and present the proposal again.

Apply only what was approved. Before editing, check that the target file did not change
since the analysis. Validate for real (run it, test it) before saying it is solved.
