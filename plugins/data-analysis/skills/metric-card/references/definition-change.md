# Changing a definition

Use when work creates, changes or discovers a definition of a metric, a dimension, a
column's meaning, a source, or a calculation rule.

1. **Find every place that cites the old rule**: search the knowledge folder, request and
   product READMEs, dataset queries and dashboard docs for the metric id, the column and
   the source name.
2. **The new rule becomes the card body**: definition, formula, filters, source, date and
   limits. Add the old column or formula to `never_use` when it became dangerous.
3. **The old rule moves to history, never deleted**: append a `history` entry (date, old
   rule, new rule, why, who decided). When the change is large, keep the full previous
   text in a `<id>-history.md` article, marked `Superseded`, with a period → rule table,
   linked from the card.
4. **Fix the other places** with a short note pointing to the current card. Do not copy
   the definition into them.
5. **Say what is still pending** (code, dataset or dashboard still on the old rule) in the
   card history or the article, so nobody assumes it is done.
6. Before using a metric in a new dataset or analysis, read the current card **and** the
   query that already exposes it: the documentation can lag behind the code. If they
   disagree, raise it with the owner before choosing.

Periods computed under different rules are never compared without saying so.
