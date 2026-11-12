# Pipeline design

## Stages (when applicable)
1. acquire from sources; 2. normalize to an internal model; 3. apply deterministic rules;
4. prepare artifact content; 5. render; 6. validate; 7. save or publish.

Keep integrations (APIs, databases, files, Spark, LLMs) separate from the rules that
select, classify, summarize and present. A smaller design is fine while it stays clear and testable.

## Migrating LLM steps to rules
An existing process that calls an LLM over a finite set of scenarios should move to conditional logic. Generic examples: a metric-change comment chosen by threshold, a slide module chosen from a JSON config, a report sent by a loop plus a template. Keep the LLM only for open-ended reasoning or free text.

## Reproducibility with mutable sources
- Record the reference date-time with time zone.
- Allow saving the normalized snapshot used for a run, and regenerating the artifact from it without hitting the source.
- Take relevant dates as parameters or a documented rule.
- Never invent missing fields: explicit fallback, or stop when the field is required.
- Selection, ordering, grouping, paging and classification rules live in versioned code or config.
- When the source lacks reliable data, use an explicit manual override and document precedence: source > config > fallback.

## Boundaries
- Separate acquisition, business rules and presentation when they change for different reasons.
- Side effects at the edges; computations operate on data passed in.
- Inject or parameterize external dependencies so rules are testable without network, DB, filesystem or LLM.
- Equivalent implementations in two runtimes: validate the shared contract with reference fixtures, not "mirror by hand".

## Where business logic lives
- Business logic belongs in the transform layer (SQL/dbt models or the rules module); the BI tool and the renderer only present. Do not recompute metrics in the dashboard or the slide builder.
- If the transform is SQL on a warehouse, prefer dbt models (skill `dbt-layered-modeling`); dbt is only the T, so ingestion and orchestration stay in this job.
