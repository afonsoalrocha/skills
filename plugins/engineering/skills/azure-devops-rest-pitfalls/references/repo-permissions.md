# Repository permissions and repo scans

Git Repositories security namespace: `2e9eb7ed-3c0a-47d4-87c1-0ffdd275fd87`. Token: `repoV2/<projectId>/<repoId>`.

| Bit | Permission |
|---|---|
| 2 | Read |
| 4 | Contribute |
| 8 | ForcePush |
| 16 | CreateBranch |
| 32 | CreateTag |
| 128 | Bypass policies when pushing |
| 512 | DeleteRepository |
| 2048 | EditPolicies |
| 8192 | ManagePermissions |

## Traps

- A Deny on a group beats an explicit Allow for a user, and can lock the owner out. For "only I write", do not deny. Turn inheritance off and grant read to the groups.
- `POST _apis/accesscontrollists` replaces the whole list. With `inheritPermissions=false` it does not copy inherited entries (the web UI does). A list without the owner locks the owner out. Always send the complete list: owner (with ManagePermissions and DeleteRepository), administrators, contributors, readers.
- Permission reads are eventually consistent. After a POST the old state may show. Wait and reread. Do not resend or send a "minimal" list.
- A user who cannot see a repository gets 404, not 403. A 404 on a repository you created means the ACL excludes you.
- A deleted or invisible repository name stays reserved: recreating it returns 409.

## Protected main with an owner who can push

- Grant the owner the push bypass bit through `accesscontrolentries` with `merge=true`, which adds without replacing the list.
- Add a blocking "Required reviewers" branch policy on main with the owner as required reviewer.
- Others clone, branch, and open pull requests. Only the owner's approval completes them.
- Set bypass before the policy: otherwise the owner cannot push to main either.
- Prefer this over rewriting the ACL of a repository already in use.

## Protocol

1. Run a dry run first and read the plan. Nothing is created.
2. Rehearse on a disposable repository, check the real effect, then do the real one.
3. Check the effect, not the `204`: query `_apis/permissions/<namespace>/<bit>?tokens=<token>` for the owner, and `effectiveAllow` on the ACL for each group. Fail if they differ.
4. Deleting a repository is irreversible. Confirm with the user, check it is empty or saved, and run `git bundle` before.

## Scan repositories without cloning

- List repositories, and read `defaultBranch` for each. It varies (`main`, `master`, others).
- List the tree through the API with full recursion. Extension and size come with the listing.
- Download text only: source, SQL, infrastructure, YAML, JSON, Markdown, shell, TOML, notebooks without outputs.
- Skip binaries and large artifacts: images, archives, spreadsheets, PDFs, state files, dependency folders.
- Skip text files over 1 MB and record them as skipped.
- Save results to a file from a saved script. Do not carry bulk data through the chat.
- Report what was ignored, by extension. No finding does not mean absent from the repository.
