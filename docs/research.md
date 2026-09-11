# Research notes

Consulted 2026-09-11. External sources describe concepts and APIs, not evidence from any target. The design and implementation are original work for this repository; no existing detector implementation was copied.

- [MITRE ATT&CK T1110.003](https://attack.mitre.org/techniques/T1110/003/): spraying involves attempts across accounts with a small password set. AuthLens only observes account breadth and failures, so AL-002 is a low-confidence compatible indicator, not confirmation. Slow/distributed behavior can evade fixed windows.
- [MITRE ATT&CK T1110.001](https://attack.mitre.org/techniques/T1110/001/): repeated guessing provides a useful investigative mapping for bursts. A behavioral mapping does not establish intent or compromise.
- [OpenSSH sshd_config](https://man.openbsd.org/sshd_config): log verbosity affects available evidence; debug logging carries privacy concerns. AuthLens does not enable or require debug logs. Its supported line grammar is narrower than all OpenSSH/platform logging variants.
- [Python datetime](https://docs.python.org/3/library/datetime.html): timezone-aware datetimes provide explicit comparisons. AuthLens rejects implicit timezone assumptions and normalizes accepted records to UTC.
- [Python tomllib](https://docs.python.org/3/library/tomllib.html): Python 3.11 provides TOML parsing in the standard library. AuthLens adds a strict bounded application schema.
- [Fail2ban repository](https://github.com/fail2ban/fail2ban): an established operational response tool. AuthLens differentiates by file-based investigation and export provenance; it does not ban hosts and does not claim replacement or novelty over the wider ecosystem.

No benchmark or detection accuracy from another product is used to claim AuthLens performance. A synthetic fixture is a regression case, not a representative field evaluation.
