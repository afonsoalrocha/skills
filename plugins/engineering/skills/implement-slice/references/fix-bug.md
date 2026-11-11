# Fix a bug

1. Build a reproduction loop that stays red on this bug.
2. Shrink the case to the smallest one that still fails.
3. List hypotheses and test one at a time.
4. Write the regression test before the fix.
5. Fix the root cause. A guard that only hides the crash does not count.
6. If two fixes fail, attack the premise and redesign from first principles.
7. Record the lesson in `AGENTS.md`, or as a new test.
