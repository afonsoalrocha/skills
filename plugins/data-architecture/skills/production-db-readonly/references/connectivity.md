# Unstable connections

- A first-attempt timeout is often DNS or VPN, not the database: flush the DNS cache, reconnect the VPN, retry with backoff.
- Retry only on specific network exceptions, a bounded number of times; then fail loudly.
- Never turn a connection error into "no data" (skill `data-integrity-tdd`).
- Log the target alias and the error class, never the host credentials or connection string.
