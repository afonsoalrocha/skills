---
name: recurring-pipelines
description: "Use when creating, changing or operating a recurring data job or automation (scheduled refresh, report generator, sync): its README contract, integration mode, runtime, minimal layout and safe, repeatable execution."
---

# Recurring pipelines

One skill for all recurring jobs. Rules specific to one job live in that job's own
README/docs, not in a new skill per job. The job runs without any agent or skill at runtime.

## What the job README must answer

A newcomer should be able to run, validate and hand the job over from the README
alone. That file states, in whatever order reads clearly:

- the run command and the validation command;
- how credentials reach the process, and where outputs are written;
- whether the job is `self-contained` (copyable, explicit dependencies) or
  `project-native` (reuses shared code only through documented public interfaces,
  never by copying it);
- the runtime it is built for: `local`, `spark/databricks` or `hybrid`, implementing
  only what that choice needs;
- which sources it reads, which artifacts it produces, who uses them, and why the
  job exists.

## Invariants

- Deterministic first: anything solvable with conditions, thresholds, templates or finite rules is code, not an LLM call. AI builds and improves the scripts; production runs without it.
- Same input snapshot + config + code version = same output. Reference date comes from a parameter, never silently from the clock.
- Every run reports source, reference date, destination and outcome.
- Re-running the same reference is predictable; never silently overwrite a different artifact.
- Integrity is validated every run before publishing: missing input or integrity failure blocks; value anomalies warn at the end (skills `data-integrity-tdd`, `data-quality-gates`).
- Read-only by default: `plan`, `preflight`, `check-sources` modes write nothing; `run`, `retry`, `reprocess` only on explicit request.
- Never delete success markers, incomplete markers or lock files to get past a validation; check the lock's PID first.
- Partial failure: retry the failed units, not the whole job.
- Credentials from environment or a secret store; never in code or versioned snapshots.
- Logs in ASCII (`OK`, `ERROR`, `WARN`, `DIFF`) with level and timestamp.
- Behavior, dependency or flow change updates the README/docs in the same change.
- No `tmp/` dumping grounds; local `output/` is for development and gitignored.

## Minimal layout

`README.md`, `requirements.txt` (or `pyproject.toml`), `main.py`, `src/`, `docs/`;
add `config/`, `tests/`, `templates/`, `output/` when useful. Python follows skill `python-data-scripts`.

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| Designing the pipeline stages, snapshots of mutable sources, architectural boundaries | `references/pipeline-design.md` |
| Writing code and tests for the job (function size, types, duplication, risk-based tests) | `references/code-and-tests.md` |
| Job produces slides, PDFs or documents for people | `references/stakeholder-artifacts.md` |
| Operating an existing scheduled job: status, retry, scheduling, diagnosis | `references/operating.md` |
| Scaffolding run modes (`plan`, `preflight`, `run`, `retry`) | `scripts/run_modes_skeleton.py` |
