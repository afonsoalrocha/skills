---
name: share-web-links
description: Use when a file in a locally synced SharePoint or OneDrive library must be referenced for a person who cannot open your disk (ticket, wiki, email, chat, deck). Compute a web link with a script; never hand over a drive path or a file:/// URL.
---

# Share web links

## Objective

Anything a stakeholder reads must open from their browser. A local path
(`C:\...`, `/home/...`) or a `file:///` URL only works on your machine.

## Invariants

- Never put a local path or `file:///` URL in a ticket, wiki page, email or message.
- Compute the link with `scripts/web_link.py`. Do not assemble it by hand: encoding and
  the type letter are the usual mistakes.
- Tenant, site, library and the local sync root come from environment variables or
  arguments, never from the skill text or from code (`references/sharepoint-url.md`).
- The URL pattern is an **observed convention**, not a documented contract. Open the
  generated link once in a browser before sharing a batch of them.
- A link proves the path, not access: the reader still needs permission on the library.
- In an HTML-capable ticket, embed the link as `<a href="URL">descriptive text</a>`;
  the text says what the file is, never the bare URL.
- Resolve the link after the file is saved in its final place. A moved file breaks it.

## Flow

1. Confirm the file lives under the synced root and is final.
2. Run `python scripts/web_link.py "<full local path>"` (set the environment first).
3. Open the link, or ask the owner to, when it is the first link of this library.
4. Paste only the link (with descriptive text) where the stakeholder reads.

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| URL pattern, extension to type letter map, encoding, environment variables, caveats | `references/sharepoint-url.md` |
| Computing a link, or testing the helper | `scripts/web_link.py` (`--help`, `--self-test`) |
