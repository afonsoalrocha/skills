# SharePoint web link pattern

Observed convention for files in a document library synced to a local folder. Microsoft
does not document it as a stable contract, so verify a sample link in a browser.

## Pattern

```
https://<tenant>.sharepoint.com/:<type>:/r/sites/<site>/<library>/<relative path>?csf=1&web=1
```

- `<tenant>`, `<site>`: the tenant host prefix and the site name.
- `<library>`: the library name as it appears in the URL (often `Shared Documents`),
  optionally followed by a folder when the sync root is a sub-folder of the library.
- `<relative path>`: the file path below the local sync root, with `/` separators.
- Every path segment is URL-encoded: space becomes `%20`, `&` becomes `%26`, and so on.

## Type letter

| Extension | Letter |
|-----------|--------|
| `.pdf` | `b` |
| `.docx`, `.doc` | `w` |
| `.xlsx`, `.xls` | `x` |
| `.pptx`, `.ppt` | `p` |
| images (`.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`) | `i` |
| `.md`, `.txt`, `.csv` | `t` |
| anything else | `u` |

## Configuration

The helper reads environment variables; each has an argument that overrides it.

| Variable | Argument | Meaning | Example |
|----------|----------|---------|---------|
| `SHARE_TENANT` | `--tenant` | tenant prefix | `my-tenant` |
| `SHARE_SITE` | `--site` | site name | `my-site` |
| `SHARE_LIBRARY` | `--library` | library path in the URL, unencoded | `Shared Documents/Team` |
| `SHARE_LOCAL_ROOT` | `--local-root` | local folder that maps to the library path | the synced folder |

If any value is missing the script exits 2 and names the missing setting.

## Example

Local root mapped to `Shared Documents/Team`, file `reports/q1 summary & notes.pdf`:

```
https://my-tenant.sharepoint.com/:b:/r/sites/my-site/Shared%20Documents/Team/reports/q1%20summary%20%26%20notes.pdf?csf=1&web=1
```

## Caveats

- Several libraries can map to several local roots: pass the matching pair per call.
- A file outside the local root is an error, not a guess.
- Sync lag: a file just saved may not exist online yet; wait for the sync to finish.
- Sharing settings are separate: the link does not grant access.
