# Metrics that guide the refactor

| Metric | Limit | Action |
|---|---|---|
| CRAP (complexity times missing coverage) | below about 10 | cover it with tests, or split the function |
| Duplication | similarity 0.8 or higher | unify the logic |
| Surviving mutants in critical modules | zero | see `../../implement-slice/references/mutation-testing.md` |
| File size | under 500 lines | split by responsibility |

Record the numbers before and after. That is how the system owner sees the effect without reading code.
