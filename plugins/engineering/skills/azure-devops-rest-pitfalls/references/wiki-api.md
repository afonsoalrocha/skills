# Wiki API

Base: `https://dev.azure.com/my-org/my-project/_apis/wiki/wikis/{wikiId}/pages`, `api-version=7.1`.

## Paths

- The real page path can differ from the URL slug. A page at `/My Section` appears as `My-Section` in the browser URL. When unsure, read `path` from `GET .../pages/{pageId}?includeContent=false`.
- A subpage uses the full path including its parent: `/My Section/Sub Page`.
- Encode the path in the API URL with `urllib.parse.quote(path, safe="/")`. `&` is literal in the path.
- For `gitItemPath` (git item view of the wiki repository), a literal hyphen is `%2D` and a space is `-`. This applies to that path format only.

## Create and update

- Create: `PUT ...pages?path={encoded}` with body `{"content": "..."}`. Create parent pages first if missing.
- Update an existing page: GET it to obtain the `ETag` header, then PUT with `If-Match: <etag>`. Without it the PUT fails.
- On HTTP 409, fetch the current ETag and retry once with the new value.
- Reread the page after publishing. A success status is not proof of the content.

## Delete

`DELETE ...pages?path={encoded}&comment=message&api-version=7.1`. Delete subpages first, then the parent. Deleting is hard to undo: confirm first.

## Links from work items

A work item references the published page URL, embedded as `<a href="URL">title</a>`. Never a repository path.
