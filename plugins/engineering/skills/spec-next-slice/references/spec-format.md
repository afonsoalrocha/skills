# Format of the next-slice spec (about one page)

```text
# Slice N: <name>
Problem: <one sentence: what it solves and for whom>
Out of scope: <what waits until later>
Decisions: <short list; hard decisions become an ADR>
Test points: <public interfaces through which behavior will be checked>
Acceptance criteria: <see acceptance-tests.md>
Risks: <money, data, migrations, an irreversible change?>
```

Precision lives in the tests, not in the paragraphs (Akita): if a sentence does not become a test, it probably does not belong.
