---
name: azure-devops-rest-pitfalls
description: "Use when automating Azure DevOps through REST or the az CLI: work item PATCH, tags, links, board columns, priority, wiki pages, repository permissions, or scanning repositories without cloning."
---

# Azure DevOps REST pitfalls

Objective: avoid the traps that make Azure DevOps automation silently do nothing, or lock people out. Examples use `my-org`, `my-project`, `repo-x`. API version `7.1`.

## Invariant rules

- Work item PATCH uses `Content-Type: application/json-patch+json`. WIQL uses system field names such as `[System.Title]` and `[System.State]`.
- Links in comments and descriptions are embedded HTML (`<a href="URL">text</a>`), never a bare URL. Documentation referenced from a work item points to the published wiki page, not a repository path.
- `System.Tags` is one text field separated by `; `. To remove a tag, filter the list and PATCH `replace`. `az ... --fields System.Tags=...` does not remove reliably.
- The board Doing/Done split is set only through the board's WEF column field. `System.BoardColumnDone` is read-only.
- Backlog order is `Microsoft.VSTS.Common.BacklogPriority`: lower value, higher on the board. Space values apart and insert at the midpoint.
- Wiki update needs the ETag from GET sent as `If-Match` on PUT. The real page path can differ from the URL slug.
- Repository permissions: never add Deny on a group, and never POST an ACL list by hand without a dry run. A bad list can lock the owner out.
- A 204, or any success status, is not proof. Reread the target after every mutation: work item, tags, wiki page, ACL, effective permission.
- Reads of permissions are eventually consistent. Wait and reread. Do not repeat the POST.
- Deleting a repository is irreversible. Save a `git bundle` first and confirm with the user.
- Credentials come from the environment or a git-ignored file, never from the repository.

## Routes

| If the task is | Read |
|---|---|
| work item PATCH, WIQL, tags, link types, board column Done, priority, `az` CLI | `references/work-items-rest.md` |
| wiki pages: publish, update, delete, paths, encoding | `references/wiki-api.md` |
| repository permissions, protected main, 404 or 409 on repos, scanning repos without cloning | `references/repo-permissions.md` |
