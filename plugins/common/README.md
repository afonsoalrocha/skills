# common

Cross-domain skills. `new-request` and `close-request` open and close a formal numbered request. They ship together: closing calls `new-request`'s `scripts/registry.py`. The other skills (session handoff and retrospective, web links, stakeholder deliverables, meeting minutes) stand alone.

| Skill | What it is for |
|---|---|
| [new-request](skills/new-request/SKILL.md) | Frame, spec, register, and move a request. |
| [close-request](skills/close-request/SKILL.md) | Close a request only after explicit human approval. |
| [session-handoff](skills/session-handoff/SKILL.md) | Save or resume the state of a work session. |
| [session-retrospective](skills/session-retrospective/SKILL.md) | Review agent sessions and propose small fixes. |
| [share-web-links](skills/share-web-links/SKILL.md) | Compute web links for stakeholders instead of disk paths. |
| [stakeholder-deliverables](skills/stakeholder-deliverables/SKILL.md) | Build PDFs and decks from approved templates and review them. |
| [meeting-minutes](skills/meeting-minutes/SKILL.md) | Turn a transcript into minutes. |

Planned, and not in the tree yet:

- `architecture-decision-record` (shared: a software reference maintained with engineering, and a data reference maintained with data architecture)

Names are indexed in the repository [README](../../README.md).

## Requirements

`registry.py` needs PyYAML. Closing a request runs that script from `new-request`, so install both skills.
