# Implementation cycle

1. Write the test at the agreed point and watch it fail for the expected reason.
2. Make the smallest change that passes. Do not tidy yet. Tidying is the `refactor-slice` skill.
3. Run the typecheck and the tests for the file at every step. Run the full suite at the end.
4. A small commit: why, what changed, and how it was proven.
5. Repeat until the slice's acceptance tests pass.

Testing rules:

- Test behavior through the public interface, never internal details.
- If the test would still pass when every function returns nothing, throw it away.
- On the critical path, test a real scenario: concurrency, a partial failure, a process dying in the middle.
- Coverage is a signal, not a target.
- A flaky test is a broken check. Fix it before anything else.
