# Work items over REST

## WIQL and PATCH

- WIQL looks like SQL. Fields are `[System.Id]`, `[System.Title]`, `[System.State]`, `[System.AssignedTo]`, with `@Me` for the caller.
- Create and update send a JSON Patch array with `Content-Type: application/json-patch+json`.
- Auth is Basic with an empty user and a personal access token as password.

```
GET   https://dev.azure.com/my-org/my-project/_apis/wit/workitems/{id}?api-version=7.1
PATCH https://dev.azure.com/my-org/my-project/_apis/wit/workitems/{id}?api-version=7.1
[{"op": "replace", "path": "/fields/System.Tags", "value": "tag-a; tag-b"}]
```

## Tags

- `System.Tags` is free text separated by `; `.
- Add: read the field, split on `;`, trim, append, join with `; `, PATCH `replace`.
- Remove: read, filter the list (compare case-insensitively), join, PATCH `replace`.
- `az boards work-item update --fields "System.Tags=..."` does not replace or remove reliably. Use REST.
- Reread the tags after the PATCH to confirm.

## Link types

| Meaning | referenceName |
|---|---|
| Predecessor (the other item blocks this one) | `System.LinkTypes.Dependency-Reverse` |
| Successor (this item blocks the other) | `System.LinkTypes.Dependency-Forward` |
| Related | `System.LinkTypes.Related` |
| Parent | `System.LinkTypes.Hierarchy-Reverse` |
| Child | `System.LinkTypes.Hierarchy-Forward` |

## Comments and descriptions

Embedded HTML links only: `<a href="URL">short text</a>`. A bare URL is wrong. For documentation, link the published wiki page. A repository path may be unreadable to the assignee.

## Board column Doing/Done

- The state does not change between Doing and Done. The split is a board field.
- `System.BoardColumnDone` is read-only. Set the board's WEF field, named like `WEF_<board-guid>_Kanban.Column.Done`.
- Find the exact name by reading the item with `$expand=all`. The GUID differs per board.
- Reread after the PATCH.

## Priority

- `Microsoft.VSTS.Common.BacklogPriority`: lower is higher on the board. Board position is the source of truth.
- List with `ORDER BY` that field ascending. Do not reorder by date or id unless asked.
- Reorder by writing values spaced far apart (for example 1000) and, when inserting between two items, the midpoint. This avoids collisions and a full renumber.
- Reread the order after reordering.

## az CLI

- Set defaults once: `az devops configure --defaults organization=https://dev.azure.com/my-org project=my-project`. The token goes in `AZURE_DEVOPS_EXT_PAT`.
- Handy: `az boards work-item show --id N`, `az boards query --wiql "..."`.
- Prefer REST or a saved script when the operation repeats.
