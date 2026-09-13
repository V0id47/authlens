# Portfolio statement

## What I built

AuthLens is an offline authentication investigation CLI developed with AI assistance and publicly released on GitHub as v0.1.0. The implemented version includes bounded SSH/JSONL ingestion, a Python correlation engine, evidence provenance, five exporters, four language catalogs and automated tests. It is a portfolio security tool, not a deployed SOC product.

## Problem

Turn an authorized local log export into inspectable investigation leads without sending the data to another service or requiring a SIEM deployment.

## Technical challenges

Explicit UTC and legacy timestamp semantics; host/service/account isolation; efficient windows checked against an independent oracle; safe partial-input status; malformed record handling; package-resource localization; HTML/CSV safety; and reliable stdout/file/log behavior across failure paths.

## Security concepts

Authentication failure patterns, conservative ATT&CK mappings, qualitative confidence, evidence versus inference, input trust boundaries, resource limits, data minimization and false-positive analysis.

## Technologies

Python 3.11+, standard library, dataclasses, deque/Counter, JSON/TOML, pytest/coverage, Ruff, Bandit, pip-audit, Gitleaks, Python wheels and GitHub Actions. The hosted test matrix passes on Ubuntu, Windows and macOS with Python 3.11–3.14. Actual validation status is in release-readiness.md.

## What I learned

Working through AuthLens taught me to treat authentication patterns as investigation leads rather than verdicts. I learned to keep observed evidence, inference, hypothesis and recommendation separate, and to document benign explanations instead of presenting every threshold match as a confirmed attack.

I also learned why UTC normalization, inclusive time boundaries and strict grouping by host, service, account and source matter in sliding-window detection. Comparing the optimized deque-based engine with an independent oracle showed me that performance improvements still need a simpler reference implementation to verify correctness.

The release process reinforced that security tooling includes more than detection logic. Bounded input, predictable exit codes, escaped reports, source hashes and careful error handling are part of the security model. A credible public release also needs a clean build, cross-platform CI, dependency and secret scans, checksums, and a fresh installation of the same artifact users will download.

## Short description for CV / LinkedIn

“AuthLens v0.1.0: herramienta pública de análisis offline de autenticaciones con parsers SSH/JSONL, correlación temporal en Python, evidencia trazable, reportes multilingües y CI en Linux, Windows y macOS. El proyecto documenta sus decisiones de arquitectura y sus límites de detección.”
