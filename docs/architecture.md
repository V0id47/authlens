# Architecture and internals

`cli` selects a language, reads one bounded TOML file and merges explicit overrides. `Settings.from_mapping` is the validated external boundary; callers constructing `Settings` directly are trusted internal code. Unknown options never become dynamic behavior.

`safeio.open_input` checks regular-file metadata before/after open. `ingest` reads bounded binary lines and hashes the exact bytes (including CRLF/BOM), decodes UTF-8, invokes the selected parser and collects quality counters. Source SHA-256 plus physical line number forms each event reference. Hashing does not authenticate the source. Exclusions precede deduplication; accepted count includes both. Events are sorted by UTC/time then original line.

`engine.detect` is a pure function. Source queues and username counters implement account breadth; account queues implement bursts and success correlation. Expired events leave each accessed queue before evaluation. Unvisited groups retain bounded state until analysis ends; memory is O(n), not O(window). Sorting is O(n log n), correlation O(n) excluding bounded evidence samples and key bookkeeping. A set suppresses later episodes per rule/group. Event/finding objects are immutable dataclasses.

`reporting.make_report` attaches localized explanations to stable machine fields. All exporters consume that model. No parser emits HTML; no detector imports CLI. The report is materialized in memory, so large limits can amplify RAM usage. JSON is authoritative. Empty CSV cannot encode run metadata because it has no finding rows.

`new_output` creates files exclusively. Reports finalize/flush/fsync before logging completion. On failure, only the newly created incomplete report is removed; lifecycle logs are retained, including safe failure codes when the medium permits. A disk error may also prevent the failure log from being written. Failed stdout is redirected to the null device to prevent Python's shutdown flush from overriding the exit code.

See [repository tree](repository-architecture.md), [spec](product-specification.md), and [security model](security-model.md). Extension rule: add a parser only when its native fixtures and semantics can be validated; do not add a generic plugin loader as speculative infrastructure.
