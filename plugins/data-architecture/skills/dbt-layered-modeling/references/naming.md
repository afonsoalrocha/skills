# Naming conventions

With 20 models anything works; with 200 nobody knows what is what. A convention keeps an
organized project organized and lets humans and agents find existing logic.

## Models and folders
| Layer | Folder | Pattern | Example |
|-------|--------|---------|---------|
| staging | `models/staging/<source>/` | `stg_<source>__<entity_plural>` | `stg_shop__orders` |
| base (optional, pre-staging dedupe/union) | `models/staging/<source>/base/` | `base_<source>__<entity>` | `base_shop__orders_deleted` |
| intermediate | `models/intermediate/<domain>/` | `int_<entity>_<verb_or_purpose>` | `int_orders_complete_months` |
| mart | `models/marts/<domain>/` | business entity or question; `fct_`/`dim_` optional | `orders`, `fct_orders`, `monthly_commerce` |
| audit | `models/audit/` | `audit_<what_is_checked>` | `audit_monthly_reconciliation` |

- Double underscore separates source from entity in staging. A project with exactly one source system may drop it (`stg_orders`); decide once and record it.
- Plural table names.
- No department prefixes on marts (they breed duplicates); time rollups belong to metrics, not model names.

## Columns
- Primary key `<object>_id` (`order_id`, never bare `id`); store keys as strings to make cross-system joins safe.
- Booleans `is_` / `has_`.
- Timestamps `<event>_at` in UTC; another zone gets a suffix (`created_at_local`).
- Dates `<event>_date`.
- Money as decimal; minor units say so (`price_in_cents`).
- Column order: ids, strings, numerics, booleans, dates, timestamps.
