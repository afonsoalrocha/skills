---
name: agent-session-worktrees
description: "Use when an AI agent session starts work that needs its own branch, when several agent sessions run in parallel on one repository, or when creating, naming, committing in, merging, or removing a git worktree."
---

# Agent session worktrees

Objective: keep parallel agent sessions from mixing files, stage, and branches, and close each piece of work cleanly.

## Invariant rules

- One agent session, one worktree, one branch. Two sessions in the same folder mix disk and stage, even on different branches. Read-only sessions may stay in the main checkout.
- Name the worktree after the task id, with a suffix when two worktrees serve the same task (`task-123-part-a`, `task-123-part-b`).
- Before creating a worktree, bring the local main branch level with the remote. Never create from a stale or diverged main.
- A new worktree has no ignored files (env files, virtual environments). Copy or rebuild them before running anything.
- With an editable install, the package points at the original checkout. Inside a worktree, set `PYTHONPATH` to the worktree root when the work changes that package.
- The command that creates a worktree moves its caller into that folder. Run it from a general session, exit with the worktree kept, then start the work session in the folder. Never delegate creation to the new session.
- The general session on the main checkout organizes the backlog and opens work sessions. It never stays inside a worktree.
- Some harnesses refuse compound commands that might touch git outside the worktree. Run simple, separate commands from the worktree folder.
- Commit per theme with selective staging, check the staged file list first, and push after every commit. Merge the main branch into yours at the start.
- Shared index files: add only your own block, do not reorder or reformat. On conflict keep both sides.
- Integrate with `merge --no-ff`, push, remove the worktree, delete the local and remote branch.
- Never discard changes without confirming what would be lost.

## Routes

| If the task is | Read |
|---|---|
| creating, naming, syncing, integrating, or removing a worktree | `references/lifecycle.md` |
| splitting work across sessions, environment gaps, commit hygiene, conflicts in shared files | `references/session-hygiene.md` |
