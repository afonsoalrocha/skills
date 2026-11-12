# Articles: update, create, split, and the agent-ready standard

## Update, create or split

Update an existing article when the learning complements the same topic, the page stays
easy to scan, and the main audience does not change.

Create a new article when the topic has a life of its own, several requests will cite it,
it would mix very different audiences, or it needs its own published path.

Split an article when agents start needing selective reading, it mixes business, dashboard
and engineering detail, sections can be read independently, or "where do I find X?" stops
having an obvious answer.

## Agent-ready standard

Agents read whole articles into context, so size and history cost tokens and add noise.

- **Size budget**: keep each article short. The check script warns above a target size and
  flags articles to split when touched (defaults are configurable; agree them per project).
- **Current summary on top** (a short paragraph or table): what holds today, rules and
  limits that change an answer, what was superseded.
- **Current separate from history**: chronological notes, superseded decisions, pilots and
  delivery evidence go to `<name>-history.md` (or `<name>-<theme>.md`), linked from the top.
- **Summary as index**: when sub-articles exist, the main article has a "Need → article"
  table so an agent opens only what it needs.
- **Split without losing content**: move whole sections by script or line ranges, confirm
  no non-empty line was dropped, keep relative links valid, and register each sub-article
  in the index.
- **Changed rule**: the main article states only the current rule (with a "never use" note
  when an old column or formula became dangerous). The previous rule stays complete in the
  history sub-article, marked `Superseded`, with a period → rule table and a link back.

## Writing

- Start with context and purpose, then details. Relative links between articles.
- Include sources, date or period, assumptions and limits.
- Say what is still pending (code or dashboards still on an old rule) in the article itself.
- Do not record ephemeral operational noise; record what saves time next time.
