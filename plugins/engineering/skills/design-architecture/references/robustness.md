# Robustness, which has to be asked for

The agent implements the happy path and waits to be told (Akita). Require the following when there is I/O or concurrency:

- A timeout on every external call.
- Retry with backoff only for specific, transient failures.
- Idempotent operations. An idempotency key on payments and webhooks.
- An atomic claim, and locks with a TTL, on jobs.
- Rate limiting and input validation.
- Secrets out of git, in environment variables or a vault.
- Errors that carry context, and are never swallowed.
