# Sanitized handoff

Use this when the person who needs the code cannot open the repository (no account, no
access). The repository stays the canonical source; the handoff is a copy.

## Steps

1. Build a copy of what the recipient needs: scripts, configuration, SQL files and
   instructions to run them.
2. Leave out `.env` files, tokens, keys, credentials and connection strings. Ship an
   example config with placeholders instead.
3. Write a manifest of file hashes (for example SHA-256 per file) good enough to confirm
   the recipient reproduces the same delivery.
4. Run the gate on the copy, not only on the repository:
   `scripts/leak_scan.py --require-denylist --denylist <private_file> <copy_path>`, plus a
   secret scanner. Fix every hit and rerun until clean.
5. Place the copy where the recipient can read it and compute a web link for it.
6. In the ticket or message, insert only the link, never the files or a local path.

## Rules

- The copy is read-only for the recipient; changes come back through the repository.
- A new version of the delivery means a new copy and a new manifest, not an edit in place.
- If the gate cannot run, the copy is not delivered.
