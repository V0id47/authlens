# First investigation in five minutes

1. Install locally following the README.
2. Run `authlens analyze examples/events.jsonl --lang en`.
3. Check input counts and source SHA-256 before interpreting indicators.
4. Inspect AL-001 and AL-003 evidence: same host, service, source and account, then success.
5. Run `authlens analyze examples/events.jsonl --format html --output demo.html --lang es` and open the new HTML locally.
6. Run with `--exclude-cidr 198.51.100.0/24`; AL-002 disappears and five exclusions are visible. This is scope removal, not proof those events were benign.

For your own data, work on an immutable authorized export. Select `--input-format ssh` only for the documented OpenSSH lines; otherwise normalize to JSONL. Never silently relabel an arbitrary Windows/VPN export as this format.

```json
{"timestamp":"2026-09-11T12:00:00Z","host":"lab","service":"ssh","username":"alice","source_ip":"192.0.2.10","outcome":"failure"}
```

Exactly these six string keys, one object per line. `outcome` is failure or success. Duplicate/unknown keys, missing offset, invalid IP, control characters and overlong fields are rejected. See configuration and product specification for grammar and bounds. A file with no indicators can still be partial: inspect `input.complete` and the process exit code.
