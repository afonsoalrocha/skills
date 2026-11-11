# Operating an existing scheduled job

- Read state before acting: the job's status file (last run, last success, pending units) and its run folder. The job-specific runbook lives in its `docs/`.
- Read-only by default: `plan`, `preflight`, `check-sources`. Writing modes only on request.
- Partial failure: prefer `retry` of pending units the same day over a full rerun.
- Never delete success/incomplete markers or the lock file to bypass validation; verify the lock owner's PID first.
- Scheduling: the scheduled run uses a plain wrapper (cron, systemd timer, Task Scheduler, CI schedule, orchestrator) that handles auth, execution and bounded retries, with no agent involved.
- When a run is not clean, an agent may be invoked for read-only diagnosis: what failed, what was published, next step; then wait for confirmation.
- A session hook or an agent never replaces the job: long deterministic execution stays in the job.
