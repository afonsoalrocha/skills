# When to scale

- Measure first: which resource saturates (CPU, memory, database, I/O), and at what load.
- The cheap move first: an index, a query, a local cache, a larger server.
- Only then split services, add an external queue, or add replicas. Each step is justified by a measurement and recorded in an ADR.
- Post-deploy is part of development. Feedback from real use is worth more than an internal review (Akita).
