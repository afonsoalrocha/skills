# common

Cross-domain skills. `new-request` and `close-request` open and close a formal numbered request. They ship together: closing calls `new-request`'s `scripts/registry.py`.

| Skill | What it is for |
|---|---|
| [new-request](skills/new-request/SKILL.md) | Frame, spec, register, and move a request. |
| [close-request](skills/close-request/SKILL.md) | Close a request only after explicit human approval. |

Planned, and not in the tree yet:

- `architecture-decision-record` (shared: a software reference maintained with engineering, and a data reference maintained with data architecture)

Names are indexed in the repository [README](../../README.md).

## Requirements

`registry.py` needs PyYAML. Closing a request runs that script from `new-request`, so install both skills.
