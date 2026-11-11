# Migrations that do not break the previous version (expand-contract)

1. Expand: add the new column or table without removing the old one.
2. Write to both. Migrate the data in batches.
3. Switch reads to the new shape.
4. Contract: remove the old one in a later deploy, after confirming.

Each step is a reversible deploy. Take a backup before any destructive step. A human review is required.
