# ADR 0002 — Stable machine schema with localized narratives

Accepted 2026-09-11. JSON schema 1.0 is authoritative. Stable IDs, enums, hashes, IPs and field names do not translate; narratives come from packaged catalogs. Exporters consume the same model. This preserves scripting while supporting four human languages.

Evidence references use source SHA-256 + physical line and bounded normalized event samples. Raw lines are omitted to avoid suffix disclosure and output amplification. This costs direct raw-text inspection: analysts consult their retained source export. Hashes identify content, not authenticity. Confidence is qualitative; no numeric certainty or CVSS is invented. CSV without findings cannot encode run metadata; use JSON for that case.
