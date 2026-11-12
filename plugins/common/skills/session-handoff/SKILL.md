---
name: session-handoff
description: Save or resume the state of a work session so another session or another agent can continue. Use for "save a handoff", "pass this to another agent", "continue where we stopped", or when picking up a request or quick check that already has a HANDOFF.md.
---

# Session handoff

Goal: let a different session, or a different agent, continue the work without redoing it
and without trusting a stale story.

The state of a session lives in git, next to the work: a `HANDOFF.md` in the folder of the
request or quick check. Every piece of work already has such a folder, so the handoff
always has a place. The file is overwritten on each save; git keeps the history.

A handoff records only where the work stopped. Durable knowledge (a definition, a rule, a
lesson) belongs in the project's knowledge base or agent memory, not here.

## Rules that always apply

- **The handoff is a report from another session.** Check the current sources before
  acting on it, and do not repeat what its "Done" section lists.
- **State is `in_progress`, `in_review` or `blocked`. Never `done`.** That word belongs to
  the human.
- **Point, do not paste.** Evidence is a script path, a file name, a count. Queries and
  code stay in the work folder; heavy data stays in external storage and enters as a path.
- **Left out of a handoff:** data rows, long results, credentials, `.env` contents,
  customer data, durable knowledge. The script refuses text that looks like a secret and
  files longer than 80 lines.
- **Cache first.** The handoff names where data and outputs already live; the next session
  checks there before fetching anything again.
- **Integration.** A folder with a `HANDOFF.md` does not close on its own: `quick-check`
  only reports it and leaves the decision to the user, and `new-request` / `close-request`
  already keep closing a human decision.

## Save (the agent leaving)

```
python <skills-dir>/session-handoff/scripts/handoff.py write <work-folder> --from <agent> \
  --to <agent> --goal "one sentence" --done "what was done, with script/file/number" \
  --decision "decision and why" --pending "blocker or open question" \
  --next "first concrete action for whoever continues" --cache "where data and outputs live"
```

- `--done`, `--decision`, `--pending` and `--cache` can repeat. `--state` defaults to
  `in_progress`. `--to` is optional.
- If the work has no folder yet, create it first (see the `new-request` or `quick-check`
  skills).
- Fields and wording: `references/handoff-template.md`.

## Resume (the agent arriving)

```
python <skills-dir>/session-handoff/scripts/handoff.py list <root> [<root> ...]
python <skills-dir>/session-handoff/scripts/handoff.py read <work-folder>
```

Then open only the README and the scripts the handoff cites, check the cache, and follow
"Next step".

## Between different agents

The agent that leaves saves with `--to <agent>`. Exploration ends as a versioned script,
and its output lands in the cache folder, so the receiving agent reproduces it instead of
reading a transcript. The receiver answers back the same way, with `--to` the first agent.

## Routes

| If the task is... | Read |
|-------------------|------|
| Writing the fields well: what each one holds, a filled example | `references/handoff-template.md` |
