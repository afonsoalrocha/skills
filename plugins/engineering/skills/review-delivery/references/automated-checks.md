# Automated checks (pre-commit and CI)

On every push: formatter, lint, typecheck, unit tests, integration tests, acceptance tests, and a security and dependency scan.

On critical modules, also: CRAP, duplication, and mutation testing.

A red check blocks the delivery. Never disable a check to make it pass.
