# Portfolio statement

## What I built

AuthLens is an offline authentication investigation CLI developed with AI assistance. The implemented version includes bounded SSH/JSONL ingestion, a Python correlation engine, evidence provenance, five exporters, four language catalogs and automated tests. It has not been represented as a deployed SOC product.

## Problem

Turn an authorized local log export into inspectable investigation leads without sending the data to another service or requiring a SIEM deployment.

## Technical challenges

Explicit UTC and legacy timestamp semantics; host/service/account isolation; efficient windows checked against an independent oracle; safe partial-input status; malformed record handling; package-resource localization; HTML/CSV safety; and reliable stdout/file/log behavior across failure paths.

## Security concepts

Authentication failure patterns, conservative ATT&CK mappings, qualitative confidence, evidence versus inference, input trust boundaries, resource limits, data minimization and false-positive analysis.

## Technologies

Python 3.11+, standard library, dataclasses, deque/Counter, JSON/TOML, pytest/coverage, Ruff, Bandit, pip-audit, Gitleaks, Python wheels and GitHub Actions. The hosted test matrix passes on Ubuntu, Windows and macOS with Python 3.11–3.14. Actual validation status is in release-readiness.md.

## What I learned

This section must reflect the owner's own study, not experiences invented by an assistant. The code and docs provide exercises: explain why five failed accounts do not prove password spraying; derive the inclusive-window test; trace a line into a finding; reproduce the closed-pipe regression; and measure the effect of a threshold/exclusion change. After doing them, replace this paragraph with your actual observations.

## Short description for CV / LinkedIn

“AuthLens: analizador offline de autenticaciones con parsers SSH/JSONL, correlación temporal en Python, evidencia trazable, reportes multilingües y pruebas de límites, falsos positivos y manejo de errores. El proyecto documenta sus decisiones de arquitectura y sus límites de detección.”

Do not add user counts, field accuracy, time saved, production deployments or publication claims unless separately demonstrated.
