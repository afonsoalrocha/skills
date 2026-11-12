# Worktree lifecycle

## Choose the isolation

| Situation | Do |
|---|---|
| Planned work with a task id | Worktree named after the task id |
| Short check, only session open, no shared code touched | May stay on the main checkout |
| Short check in parallel with another session | Worktree |
| Shared code (tooling, skills, rules, project instructions) while another session is open | Short-lived worktree, fast merge |
| Two sessions on the same code, different parts | One worktree per part, with part suffixes |
| Read only, no commit | Main checkout |

A branch without a worktree is acceptable only when you are certain no other session is open.

## Create

1. On the main checkout, make local main equal to the remote: push if ahead, fast-forward pull if behind. If it diverged, stop and ask the owner.
2. Create the worktree from the remote main, in the tool's standard worktrees folder, on a branch named after it. Do not hand-roll sibling folders.
3. Prepare ignored files (see `references/session-hygiene.md`).
4. Uncommitted files on main do not block creation. Leave files that are not yours alone.

## Work

- Start with a merge of the main branch into the work branch. A small conflict now beats a large one later.
- Commit and push as described in `SKILL.md`. Use `push -u` on the first push of a branch.

## Integrate and close

1. Merge the main branch into the work branch and resolve conflicts, keeping both sides of shared index files.
2. On the main checkout (equal to the remote and clean), run `git merge --no-ff <branch>` so history shows which work it came from.
3. Push.
4. Remove the worktree, then delete the local branch and the remote branch.
5. Stop and ask when the conflict is not trivial, another session left pending files on main, or removal would lose something.

## Remove safely

Never force-remove or discard changes before listing what is uncommitted or unpushed and getting confirmation. Prefer the least destructive option.
