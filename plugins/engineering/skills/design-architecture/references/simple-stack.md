# A simple, cheap stack

A starting point, adjusted to the problem (Akita):

- One server, a relational database or SQLite, a queue and jobs in that same database, and a container deploy.
- No microservices, external queues, distributed cache, or Kubernetes until a measurement shows the lack.
- Extract a homegrown framework only after the same pattern has been repeated across several projects. Never design it up front.
- The language matters less than having tests and checks.
