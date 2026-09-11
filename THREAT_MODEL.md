# Threat model

## Assets and boundaries

Protect original input integrity, analyst machine availability, report interpretation, sensitive identities and the ability to distinguish partial analysis from clean results. Input log text is untrusted; CLI/config and destination directories belong to the operator. A local administrator or writer controlling parent directories is outside scope. There are no remote boundaries at runtime.

| Threat | Control | Residual risk / verification |
|---|---|---|
| Hostile or oversized record | Byte/line/event ceilings, closed JSON schema, bounded diagnostics | In-memory sorting and report amplification remain; benchmark and set lower limits |
| Incorrect temporal inference | UTC, explicit traditional year/offset, reject backward traditional times | Clock skew, forged events and coarse timestamps cannot be corrected from this input |
| False incident confirmation | Separate observations/inference/hypothesis, rule rationale and benign explanations | Human validation and additional telemetry remain necessary |
| HTML/Markdown/CSV injection | Escaping, no JS/network resources, CSP, CSV prefix neutralization | Downstream tools may transform exported data; JSON is authoritative |
| Secret disclosure | Discard raw records/suffixes, diagnostics by code/line, lifecycle counts only | A username/host field can itself contain sensitive data; privacy is not anonymization |
| Input replacement/growth | lstat/open/fstat checks, regular files, nofollow/nonblock where available, final metadata/byte checks | Trusted directories required; hashing is not tamper-proof chain of custody |
| Output overwrite/link attack | O_EXCL, owner mode on POSIX, reserved output before analysis | Windows ACLs inherited; hostile parent-directory changes not defeated |
| Misleading success on failure | Dedicated codes, partial reports, reserve/finalize output before completion log | Disk failure can also prevent reliable logging; a missing/truncated log is not success |
| Command execution / unsafe deserialization | No subprocess/network in runtime, JSON/TOML only, no plugins or dynamic code | Build/development tools have separate supply-chain exposure |
| Dependency compromise | No runtime dependencies; pinned development tools and action SHAs | Python/build ecosystem still requires updates and reviewed sources |

## Abuse cases and controls to retain

An adversary can forge events to implicate a source. This analyzer cannot authenticate them; source hash identifies bytes, not truth. A legitimate shared address can trip rules; never automatically block or sanction identities. Exclusions can hide activity; effective settings appear in reports. Empty or wholly excluded files return 4, not a clean assessment. One representative episode per group is a deliberate 0.1.0 limit, not exhaustive incident enumeration.

The tool never connects to indicators, attempts authentication, loads external HTML, executes an attachment or changes target systems. No secrets are needed; `.env.example` would add no value.
