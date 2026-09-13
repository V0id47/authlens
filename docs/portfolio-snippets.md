# Portfolio snippets

These are factual drafts based on the published v0.1.0 release and its recorded validation evidence.

## GitHub description (~160 characters)

Offline authentication triage CLI: strict SSH/JSONL parsing, explainable time-window indicators, evidence provenance, safe reports and four locales.

## CV version

- Built AuthLens, an offline Python CLI that normalizes SSH/JSONL authentication exports, correlates three bounded time-window indicators and preserves source hash, quality counts and event evidence.
- Implemented text/JSON/CSV/Markdown/HTML reporting with English, Spanish, Russian and Simplified Chinese catalogs, strict configuration, safe output creation and scripting-friendly exit codes.
- Validated parser/detector boundaries, malformed input, injection-safe exporters and failure paths with 92 tests, an independent randomized oracle and 93.61% branch-aware coverage; the 12-job hosted matrix passes on Ubuntu, Windows and macOS with Python 3.11–3.14.

## LinkedIn project description

AuthLens is a publicly released offline authentication investigation tool. It turns an authorized SSH or normalized JSONL export into explainable leads for repeated failures, multi-account failure breadth and a success following failures. The implementation emphasizes evidence over claims: source hashes, line references, input-quality counters, bounded reports and explicit observations, inferences, hypotheses and benign explanations. It includes five report formats, four language catalogs, a threat model, ADRs, packaging, regression/e2e tests and a green 12-job cross-platform CI matrix. It is not a deployed SOC product or a claim of field detection accuracy.

## Interview elevator pitch (30–45 seconds)

“I built AuthLens as a local-first authentication triage CLI. It accepts a narrow SSH grammar or strict JSONL, normalizes timestamps to UTC, and uses sorted sliding windows to detect repeated failures, failures across accounts, and a success after repeated failures. Each result keeps a source hash, line references and a bounded evidence sample, while the report separates what was observed from what is inferred. I kept the runtime dependency-free, tested the optimized deque engine against an independent oracle, and validated the package on Ubuntu, Windows and macOS across Python 3.11–3.14. The important limitation is that these are investigation indicators: they do not prove password spraying or unauthorized access, and representative labeled field evaluation remains future work.”

## Claims outside the evidence

The current evidence does not support claims that AuthLens is production-ready, enterprise-grade, used by SOC teams, accurate in the field or reviewed editorially by native speakers.
