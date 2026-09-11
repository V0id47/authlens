# Detection logic and limitations

Rules version 1; defaults window 300 seconds and thresholds 5. UTC interval is inclusive. Evaluation order: timestamp then original line. At equal timestamps, a success sees failures only earlier in that order. No assertion of ordering beyond the source is possible at low time precision.

| Rule | Key | Predicate | Priority / confidence |
|---|---|---|---|
| AL-001 | host, service, source_ip, username | Failure arrives and failure count in window >= burst_threshold | MEDIUM / medium: repeated friction, no demonstrated access |
| AL-002 | host, service, source_ip | Failure arrives and distinct failed usernames in window >= spray_threshold | MEDIUM / low: breadth worth investigating, passwords unknown |
| AL-003 | host, service, source_ip, username | Success arrives after >= success_threshold failures still in window | HIGH / medium: successful access makes review more urgent, unauthorized access unproven |

Each group/rule emits once per input, at the earliest threshold crossing. Overlapping rules are retained because account breadth and per-account volume are different observations. Windows do not reset on successes: AL-003 means preceding failures within the window, not necessarily uninterrupted failures. Later incidents for the same key require a separately scoped export in 0.1.0. Do not concatenate cases expecting episode enumeration.

Evidence contains up to 20 events, preserving the first 19 and triggering last event when truncated. `event_count` includes the success for AL-003; `account_count` is exact for the full triggering window. `evidence_truncated` says when the sample is incomplete. The finding ID hashes rule/version, grouping, first/last source event IDs. Changing source bytes changes IDs even when semantic events look identical; IDs are not cross-export asset identities.

ATT&CK links are investigative context: [T1110.001](https://attack.mitre.org/techniques/T1110/001/) for repeated failures/success correlation, [T1110.003](https://attack.mitre.org/techniques/T1110/003/) for breadth. Reports never prove which passwords were attempted. Confidence is ordinal, not a probability. Severity is local triage priority, not CVSS or a confirmed vulnerability rating.

## Counterexamples and validation

- Five identical usernames do not satisfy account breadth.
- Failures at 0,1,2,3,300 seconds satisfy a 300-second burst; at 0,1,2,3,301 they do not.
- A success on another host, service, account or source is not correlated.
- A success before failures is not evidence of subsequent access.
- Repeated exact events are deduplicated by default; counters disclose the effect.

Tests compare the optimized result keys with a straightforward independent O(n²) oracle over seeded random streams. They also exercise exact hand-derived boundaries. Synthetic correctness tests do not measure production precision/recall. A representative labeled corpus is required before claims about real-world detection accuracy.

Benign causes include retries, stale automation, client misconfiguration, shared NAT, QA, SSO incidents and legitimate account recovery. Slow/distributed attempts, missing logs, clock skew, usernames with differing representations and untrusted collector data limit detection. Never automatically block an address or punish an account based on these indicators.
