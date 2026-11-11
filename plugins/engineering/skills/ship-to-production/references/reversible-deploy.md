# A deploy that is small, frequent, and reversible

- The first slice already goes to production, with CI/CD (a skeleton that walks).
- Deploy only with green CI. Tag a release only with green CI.
- Feature flags turn new behavior on separately from the deploy.
- Use staging when the risk justifies it.
- A rollback that has been tested: know the command and the time before you need them.
- Fixing it later is cheap (Akita), except for what leaves the system: payments, messages already sent, and other people's data.
