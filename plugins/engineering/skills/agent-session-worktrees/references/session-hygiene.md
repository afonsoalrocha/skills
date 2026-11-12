# Session hygiene

## General session versus work session

- The general session lives on the main checkout. It lists and prioritizes tasks, comments on them, and opens work sessions.
- The work session lives in one worktree. Its brief names the task and the branch, says to wait for instructions, and asks it to read the folder's notes and `git log` first.
- Existing worktree: start the work session with its working directory set to that folder, without asking for another worktree.
- New worktree: from the general session, create it, exit with the worktree kept, then start the work session in the folder. The create command traps its caller, so a work session that runs it can no longer return to the main checkout.

## Ignored files and environments

- Files ignored by git (env files, virtual environments, local caches) do not exist in a new worktree. Copy or link them, or rebuild, and confirm before running scripts.
- Credentials are a step for the human owner when a policy blocks the agent from copying them.
- An editable install resolves to the checkout where it was installed. A script run by path inside a worktree can import the original checkout instead of the worktree copy. Set `PYTHONPATH` to the worktree root when the work edits that package, and confirm which copy is imported.

## Harness command guards

A harness may refuse compound commands that could reach git outside the worktree. Work around it by:

- running one simple command per call, from the worktree folder
- avoiding `cd x && ...`, inline scripts that mention git, shell variables computed inside git commands, and `git ... | grep`
- writing a temporary script to the scratchpad instead of an inline heredoc

## Commits

- One commit per theme, written when the subject is finished.
- Stage selectively. Run `git diff --cached --name-only` before committing. Never `git add -A`.
- Push after every commit, on any branch.

## Shared index files

Files that several sessions append to (indexes, registries, changelogs): add only your block, keep order and formatting. On conflict, keep both sides.

## Do not touch

- Another session's worktree.
- Pending files you did not create.
- Uncommitted work you cannot explain: ask before discarding.
