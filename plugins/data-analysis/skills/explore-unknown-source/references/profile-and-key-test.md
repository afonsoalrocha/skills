# Query shapes, link test and reading the results

## Profile: one row per field

The script restricts the table to the window once (`win` CTE), computes counts per field
as stacked rows (`UNION ALL`), and picks examples by ranking distinct values with
`ROW_NUMBER()`, so the output reads top to bottom, one field per line:

```sql
WITH win AS (SELECT a, b FROM t WHERE created_at >= '2024-01-01' AND created_at < '2024-02-01'),
stats AS (
  SELECT 'a' AS field, COUNT(*) AS n_rows,
         COUNT(CASE WHEN a IS NOT NULL AND CAST(a AS VARCHAR) <> '' THEN 1 END) AS n_filled,
         COUNT(DISTINCT a) AS n_distinct FROM win
  UNION ALL ...
),
ranked AS (
  SELECT field, val, ROW_NUMBER() OVER (PARTITION BY field ORDER BY val) AS rn
  FROM (SELECT DISTINCT 'a' AS field, SUBSTRING(CAST(a AS VARCHAR), 1, 40) AS val
        FROM win WHERE a IS NOT NULL UNION ALL ...) v
)
SELECT s.field, s.n_rows, s.n_filled, s.n_distinct, string_agg(r.val, ' | ' ORDER BY r.val)
FROM stats s LEFT JOIN ranked r ON r.field = s.field AND r.rn <= 3
GROUP BY s.field, s.n_rows, s.n_filled, s.n_distinct;
```

Dialect differences handled by `--dialect`: the text type in `CAST`, and the aggregation
that joins examples (`string_agg` in DuckDB/Postgres, `concat_ws` + `collect_list` in Spark,
`GROUP_CONCAT ... SEPARATOR` in MySQL 8). Exact `COUNT(DISTINCT)` is used everywhere; when
the table is large, the cost rules and approximations of `sql-performance` apply.

## Link test: one query, both sides

```sql
WITH lkeys AS (SELECT k, COUNT(*) AS n FROM a WHERE k IS NOT NULL GROUP BY k),
     rkeys AS (SELECT k, COUNT(*) AS n FROM b WHERE k IS NOT NULL GROUP BY k)
SELECT (SELECT COUNT(*) FROM lkeys WHERE n > 1) AS left_repeated_keys,
       (SELECT COUNT(*) FROM lkeys l WHERE NOT EXISTS
          (SELECT 1 FROM rkeys r WHERE r.k = l.k)) AS left_without_match,
       ...  -- the same for the right side, plus null-key counts
```

Reading it:
- no repeated keys on either side and nothing unmatched: one-to-one link;
- repeats on one side only: one-to-many, the repeating side is the "many";
- unmatched keys on one side: coverage gap; group the unmatched rows by status or stage
  before deciding whether the gap is expected;
- many null keys: the field is conditional (see the profile table in `SKILL.md`).

## Worked example (synthetic)

Tables `support_tickets(ticket_id, channel, survey_score, state)` and
`chat_messages(message_id, thread, sender_type, sent_at)`.

- The profile shows `chat_messages.thread` values like `T-48213`, the same format as
  `support_tickets.ticket_id`. Candidate key, despite the vague name.
- Key test: every message thread matches a ticket; 1:N (many messages per ticket). In the
  other direction, some tickets have no messages: those came from the phone channel.
- `support_tickets.survey_score` is filled for a minority of tickets. Breakdown by `state`:
  filled only after a ticket is resolved. "Unresolved tickets have no score" is the rule,
  not a data gap.
- `chat_messages` has about twice as many rows as distinct `message_id`: the view adds one
  row per attachment. Count distinct ids.
- `channel` has a single distinct value in the chat table: a constant, useless as a split.

Conclusion written down: "messages join to tickets by `thread = ticket_id`; the score
exists only for resolved tickets; count messages by distinct `message_id`."
