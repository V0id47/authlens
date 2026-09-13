# Changelog

Semantic Versioning is used for tool releases. Report `schema_version` is independently versioned; breaking schema changes require explicit migration notes.

## 0.1.0 — 2026-09-13

- Added bounded offline SSH/JSONL ingestion, UTC normalization, source hashes and data-quality counts.
- Added AL-001 repeated failures, AL-002 multi-account failures and AL-003 success-after-failures indicators.
- Added text/JSON/CSV/Markdown/HTML reporting with evidence, limits and human investigation guidance.
- Added en/es/ru/zh-CN catalogs, strict TOML configuration, script exit codes and exclusive output/log creation.
- Added synthetic demos, meaningful regression/oracle/e2e tests, build configuration and CI workflows.
- During initial review, fixed oversized SSH port conversion, failed-pipe shutdown and report/log completion ordering.

Published as [AuthLens v0.1.0](https://github.com/V0id47/authlens/releases/tag/v0.1.0) on GitHub. No PyPI publication is claimed. See docs/release-readiness.md for the validation record.
