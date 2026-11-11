# Building the denylist

- Source it from the private material you are generalizing: company and product names, domains and hosts, account and resource IDs, catalog/schema/table/column names that are not generic, internal folder names, tool aliases, people, client names, internal metric names.
- One term per line, case-insensitive matching; `#` comments allowed.
- Skip terms shorter than 4 characters for substring matching (too many false positives); check short or generic words with word-boundary matching instead.
- Include variants: with/without separators (`acme-data`, `acme_data`, `acmedata`), plurals, email domain.
- Generic words that are also internal names (e.g. a team called after a common noun) go in with word boundaries and a manual review of each hit.
- Keep the list outside the repo (or gitignored) and store a copy as a CI secret; never paste it into issues, PRs or chats.
- Re-derive the list whenever new private sources are used.
