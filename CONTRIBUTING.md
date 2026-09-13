# Contributing

Start with [development setup](docs/development.md) and the [product specification](docs/product-specification.md). Keep changes focused and readable for a learner reviewing the design.

Before a feature, state its user/problem, delivered information, validation, false positives, failure modes, documentation and automatic test strategy. A detector PR includes a failing regression or synthetic positive/negative/boundary fixtures, supported fields, exact time/grouping semantics, severity rationale and an honest ATT&CK mapping. No live attack traffic or real credentials in tests.

Run lint, formatting, full tests/coverage, Bandit and build. Keep all four catalogs in sync; never translate stable keys/IDs. Update applicable READMEs and changelog. Document significant decisions as an ADR. Do not bump coverage by testing constants or mirroring the implementation.

Use descriptive commits and PRs that explain the actual behavior change and how it was checked. Do not claim external deployments, customers, benchmarks or personal learning experiences that did not occur. A portfolio owner should be able to explain and modify the work they present.

For security issues follow [SECURITY.md](SECURITY.md). For conduct issues privately contact the repository owner using an available platform channel; no response-time promise is made.
