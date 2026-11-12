---
name: new-request
description: Open a formal, numbered work request (analytics or engineering): frame the question or goal, write the spec and acceptance criteria, register it in requests/registry.yaml, or resume and move an open one. Not for one-off checks (quick-check) or closing (close-request).
---

# Open or resume a request

A request is a numbered, formal unit of work with a requester, a decision or outcome it
supports, and acceptance criteria. It serves analytics and engineering work alike. One-off
questions ("take a quick look") go to `quick-check`.

## Rules that always apply

- Read `requests/registry.yaml` before opening any request folder. It is the single index
  of requests: title, status, owner, sources, tags, key scripts.
- Register a new request the moment it is opened, even with a partial spec.
- The spec is written for a human. The human owns definitions, acceptance thresholds and
  every status change not already written in the spec. Ask instead of deciding.
- If the request uses metrics, link each metric card (skill `metric-card`). A metric without
  a card cannot appear in acceptance criteria.
- Lifecycle: `open` → `in_spec` → `in_build` → `in_interpretation` → `closed`, plus `paused`.
  Every change is an appended transition with a date and a reason; `status` equals the last
  transition. Never rewrite an earlier transition.
- The close outcome (`complete` / `partial` / `blocked`) is a separate field, set only by
  `close-request`.
- Code, queries and docs live in git. Raw extracts and heavy outputs live in the project's
  external storage, never in git and never in `tmp/` folders inside the repo.
- Cache first: reuse an existing extract or artifact when the cut and the inputs have not
  changed.

## Steps (new request)

`scripts/` paths are relative to this skill folder; run them from the project root.

1. `python scripts/registry.py next` prints the next id. Folder: `requests/NNN-short-slug/`.
2. Copy the template from `references/request-readme.md` into the folder as `README.md` and
   fill every heading.
3. `python scripts/registry.py open NNN short-slug "Title" --requester "<role>" --owner "<role>"`
   appends the entry with status `open`.
4. Read the project knowledge index and the articles linked to the topic before building.
5. Write the checks before the code they protect (data: `data-integrity-tdd`, full set for a
   request; code: the project's test skill), then build, and record results in the README.
6. Move the status with `python scripts/registry.py move NNN <status> "<reason>"`.
7. `python scripts/registry.py validate` must pass before any commit that touches the registry.

## Resuming a request

Read in this order: registry entry → README → linked knowledge articles → scripts named in
the README. Before editing, be able to say which request, which inputs, which files will
change and which check protects the change. If any of those is unclear, read more first.

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| Writing the spec: question, decision, metrics, grain, period, out of scope, acceptance criteria | `references/request-readme.md` |
| Registry fields, allowed transitions, linking an external ticket, requests that create a product | `references/registry.md` |
| Running the registry script (`next`, `open`, `move`, `validate`) | `python scripts/registry.py --help` |

Related skills: `quick-check` (one-off), `metric-card` (definitions), `close-request` (closing).
