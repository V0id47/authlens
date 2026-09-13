# AuthLens — interview review

This guide is for understanding the implementation, not memorizing a sales pitch. A strong answer names the relevant module, a concrete trade-off, an observable test, and a limitation. The questions are intentionally harder than the README.

## Architecture

### Why Python 3.11+?

**What a strong answer should contain:** The runtime is an offline parser/correlation CLI, not a high-rate network scanner. Python 3.11 gives `tomllib`, timezone-aware `datetime`, `ipaddress`, dataclasses and a readable standard-library implementation. No runtime dependencies reduce supply-chain and installation cost. The trade-offs are interpreter/runtime memory and the absence of a native single binary; those matter if the scope becomes large-scale collection.

### Why no runtime dependencies?

**What a strong answer should contain:** The tool's core needs are already covered by the standard library. This keeps an authorized log export local, makes a wheel smoke test meaningful and reduces dependency exposure. Development dependencies remain pinned and audited separately. “No dependencies” does not mean the Python/build supply chain is risk-free.

### Why separate detector, CLI and reporting?

**What a strong answer should contain:** `engine.detect` is pure over canonical `Event` objects, so it can be tested with an independent oracle and reused by every exporter. The CLI handles process boundaries and exit codes; reporting handles localization and escaping. This prevents a presentation change from changing security semantics.

### Why JSONL?

**What a strong answer should contain:** JSONL is a small, line-oriented interchange contract that can be generated offline and processed incrementally. AuthLens rejects unknown keys and implicit timestamps instead of pretending arbitrary exports are compatible. It is not a promise to understand EVTX, VPN or every syslog dialect.

### Why UTC?

**What a strong answer should contain:** Comparing aware timestamps in UTC makes offsets explicit and removes local-DST ambiguity. Traditional SSH timestamps require an explicit year and fixed offset; backwards movement is rejected rather than guessed as a year rollover. The limitation is that forged timestamps and clock skew remain input problems.

### Why sliding windows and deques?

**What a strong answer should contain:** A rule asks whether prior events remain within an inclusive interval. Deques remove expired events from the front, while counters maintain account breadth without rescanning the whole window. Sorting is O(n log n); correlation is linear after sorting. Evidence is bounded to 20 events, but the full report and sorted event list still have memory costs.

### Why an independent oracle?

**What a strong answer should contain:** The optimized deque/counter implementation could share the same mistake as its test helper. The randomized test compares it with a deliberately straightforward O(n²) predicate whose grouping, thresholds and boundary literals are independently written. It verifies behavior, not internal structure or coverage for its own sake.

## Detection

### What is the difference between AL-001 and AL-002?

**What a strong answer should contain:** AL-001 counts failures for one exact host/service/source/account. AL-002 counts distinct failed usernames for one host/service/source. The first is volume against an identity; the second is breadth. They can both fire, and neither proves intent or password reuse.

### Why is AL-003 HIGH?

**What a strong answer should contain:** A success after five same-account/source failures makes triage more urgent because access occurred in the observed records. HIGH is a local investigation priority, not CVSS and not proof the access was unauthorized. Legitimate recovery remains a documented false positive.

### Does AL-002 confirm password spraying?

**What a strong answer should contain:** No. The logs show account breadth and timing, not the attempted password, authorization context or actor. The report maps the observation to ATT&CK T1110.003 as compatible context with low confidence. Shared NAT, QA, SSO failure and authorized tests can produce the same pattern.

### What are false negatives?

**What a strong answer should contain:** Slow attempts outside the fixed window, distributed sources, missing/rotated logs, clock skew, parser dialects rejected as unsupported, and attempts using different source addresses can evade these rules. Only the first episode per rule/group is emitted in 0.1.0, so later episodes in one input are intentionally not enumerated.

### What happens at the exact boundary?

**What a strong answer should contain:** The interval is inclusive. Failures at seconds 0, 1, 2, 3 and 300 satisfy a 300-second window; a fifth at 301 does not. Events at equal timestamps are ordered by original line, so a success only sees preceding failures in that deterministic order.

## Security

### Why are raw SSH suffixes discarded?

**What a strong answer should contain:** Suffixes can contain fingerprints or collector-specific sensitive text and are not required for the v1 rules. Reports keep normalized fields, line numbers, event IDs and a source hash. Analysts must retain the authorized source export for full forensic review; minimization is not anonymization.

### How is CSV injection prevented?

**What a strong answer should contain:** Cells beginning with `=`, `+`, `-`, `@` or control/newline prefixes are prefixed with an apostrophe before CSV serialization. CSV is still a downstream format whose consumers may transform data; JSON remains authoritative.

### How is HTML injection handled?

**What a strong answer should contain:** Variable content is passed through HTML escaping, evidence is placed in escaped `<pre>` blocks, and the document has a restrictive CSP with no scripts, forms, CDN or network resources. The test uses script-looking identities and inspects rendered Markdown/HTML behavior.

### Why never overwrite outputs?

**What a strong answer should contain:** `O_EXCL` prevents accidental replacement and makes a report path an explicit operator decision. New incomplete reports are removed on failure; pre-existing files are never touched. POSIX uses mode 0600; Windows inherits directory ACLs. A hostile parent directory or local administrator is outside the trust boundary.

### What does SHA-256 guarantee, and what does it not?

**What a strong answer should contain:** It identifies the exact bytes processed by this run and is included in event IDs/provenance. It does not prove who produced the log, that the source was untampered before acquisition, or establish chain of custody.

## Engineering

### How is malformed input handled?

**What a strong answer should contain:** The parser emits a safe machine code and line number; raw values are not echoed. Non-strict mode records bounded diagnostics and returns a partial report/code 4. Strict mode stops at the first malformed record. Hard limits or source mutation produce no misleading final report.

### Why file and line limits?

**What a strong answer should contain:** They bound accidental resource exhaustion and report amplification before decoding or materializing unlimited data. Defaults are 16 MiB, 16 KiB per line and 50,000 accepted records; increases remain bounded. They are safeguards, not a fixed-memory guarantee.

### What does branch-aware coverage mean here?

**What a strong answer should contain:** Coverage.py measures statements and branch decisions, including subprocesses configured by the project. The latest local run was 93.61% with 91 tests passing and one privilege-limited skip. Coverage does not prove detector accuracy or production readiness.

### What is the difference between unit, integration, regression and e2e tests?

**What a strong answer should contain:** Unit tests isolate contracts such as parsing, config, correlation and escaping. Integration tests use real files and schemas. Regression tests preserve fixes for oversized input, pipes and finalization. E2E tests invoke `python -m authlens` as a subprocess and assert stdout, stderr and exit codes.

## Limitations and ownership

### What does AuthLens deliberately not do?

**What a strong answer should contain:** No network collection, credential attempts, blocking, EVTX/VPN/native web adapters, GeoIP/reputation, ML, plugins, dashboards, enrichment, attribution or multi-episode enumeration. These are scope decisions for 0.1.0, not hidden roadmap claims.

### What would be needed before production use?

**What a strong answer should contain:** A real repository with protected CI across supported platforms, secret scan, native-speaker review, representative labeled data and a measured evaluation, operational ownership, privacy review, release signing/provenance and human response procedures. Even then, the output would be triage evidence requiring corroboration, not an autonomous containment decision.

### Which checks demonstrate implementation understanding?

**What a strong answer should contain:** Explain and alter a threshold safely, reproduce the inclusive boundary and closed-pipe regression, inspect an event ID back to its source line, explain a false positive, run the released-wheel smoke test and identify the remaining validation limits.
