# `requests/registry.yaml`

The registry is hand-kept and is the source of truth for which requests exist and where
each one stands. Generated indexes, if any, are built from it, never the reverse.

```yaml
version: 1
requests:
  - id: "001"
    slug: short-slug
    title: Human title
    path: requests/001-short-slug
    status: in_build            # equals the last transition
    requester_role: role
    owner: role
    opened_on: 2026-01-15
    tags: [topic, source]
    sources: [source name]
    external_ticket: null       # id in the team tracker, if any
    transitions:
      - "on": "2026-01-15"
        to: open
        reason: Why it was accepted.
      - "on": "2026-01-16"
        to: in_spec
        reason: Spec started with the requester.
    # outcome: complete | partial  (only on a closed request, set by close-request)
```

## Allowed transitions

| From | To |
|------|----|
| `open` | `in_spec`, `paused` |
| `in_spec` | `in_build`, `paused` |
| `in_build` | `in_interpretation`, `in_spec`, `paused` |
| `in_interpretation` | `closed`, `in_build`, `paused` |
| `paused` | the status it was paused from |
| `closed` | `in_interpretation` (reopen, with a reason) |

Going back a step is allowed and must say why. `closed` is reached only through
`close-request`, with explicit approval from the human.

## External ticket

A request may or may not have a ticket in the team tracker. If it has one, the README cites
its id, and the ticket links to published documentation, never to internal repository
paths. A ticket that enters active development needs a request opened first.

## Requests that create a data product

The request can stay in `in_interpretation` while the product is being accepted, but the
living code already moves to the product folder. Closing the request does not retire the
product.
