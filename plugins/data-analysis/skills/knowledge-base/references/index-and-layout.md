# `knowledge/index.yaml` and layout

```
knowledge/
├── README.md
├── index.yaml
├── business/
├── metrics/          # metric cards (skill metric-card)
├── dashboards/
├── data/
├── engineering/
├── processes/
└── tools/
```

Each article entry:

```yaml
articles:
  - id: stable-id                 # never reused
    title: Human title
    layer: data                   # business | metrics | dashboards | data | engineering | processes | tools
    subject: common               # optional split by product line or area, instead of folders
    audience: analysts
    file: data/orders-sources.md
    published_path: null          # path in the published wiki, if any
    status: active                # active | superseded | retired
    summary: One line, used by agents to decide whether to open it.
    tags: [orders, source-of-truth]
    related: {metrics: [], dashboards: [], requests: [], sources: []}
```

- Every file in the layer folders is in the index, and every index entry points to an
  existing file (the check script verifies both).
- A retired article keeps its entry with `status: retired` and a pointer to what replaced it.
