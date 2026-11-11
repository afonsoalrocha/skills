# Mutation testing

Required where there is money, data, or a critical rule (Uncle Bob; a mutation tool).

- The tool changes the code on purpose (it swaps `>` for `>=`, 10% for 0%, or deletes a line) and runs the tests.
- A mutant that survives is a weak test. Write the test that kills it, or delete the dead code.
- Run it on the module that changed, not on the whole project, so the loop stays fast.
- Common tools: Stryker (JS/TS), mutmut (Python), PIT (Java), cargo-mutants (Rust).
