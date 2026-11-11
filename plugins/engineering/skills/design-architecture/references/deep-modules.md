# Deep modules, with the domain at the center

- A modular monolith. Each module has a small interface and a lot of behavior behind it (Ousterhout, via Pocock).
- The interface is the test surface. The owner and the engineer design the interface and the tests. The agent takes care of the inside.
- The deletion test: if deleting the module spreads complexity across its callers, the module is deep. If nothing changes, it is shallow and can disappear.
- One adapter is a hypothetical place to swap. Two adapters are a real one. Do not abstract before the second.
- Business rules live in pure functions at the center. The database, the network, queues, and the interface sit at the edges. Dependencies point inward (Uncle Bob).
- Validate data where it enters, and trust it inside. Use types that make invalid states impossible.
- One writer for each piece of shared state.
- Limits: CRAP below about 10 per function, and files under 500 lines. Do not chop a function up just to fit a number.
