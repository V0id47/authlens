# ADR 0001 — Python and standard-library runtime

Accepted 2026-09-11. Python 3.11+ provides timezone-aware datetime, TOML, JSON, IP parsing, dataclasses and a portable CLI without runtime dependencies. Its readability supports the owner's learning goal. The implemented computation is file parsing/sorting/correlation, not packet-rate networking.

Go was considered for single-binary distribution; Rust for low-level guarantees. Neither offsets their additional implementation cost for this bounded offline workflow. Python consumes more RAM and needs an interpreter; bounded defaults and a benchmark make that tradeoff visible. Native EVTX or large-scale streaming would require a new decision, not silent scope expansion.
