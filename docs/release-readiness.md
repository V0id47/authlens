# Release readiness — AuthLens 0.1.0

Checked 2026-09-11 on Windows 11, Python 3.12.14. This is a local release-candidate record, not a GitHub Release, PyPI publication or production certification.

| Gate | Estado actual | Evidencia | Acción | ¿Bloquea Portfolio Ready? |
|---|---|---|---|---|
| Product scope and threat model | PASS | Product spec, ADRs, `THREAT_MODEL.md`, `SECURITY.md`; three bounded offline rules and explicit non-goals | Mantener el alcance congelado en v0.1.0 | No |
| Unit/integration/regression/e2e behavior | PASS | 91 passed, 1 skipped; `python -m pytest -q` | Repetir en CI remota | No localmente; sí hasta verificar CI |
| Meaningful coverage | PASS | 93.61% branch-aware, subprocesses included; threshold 80% | Conservar el gate en CI | No localmente; sí hasta verificar CI |
| Lint and formatting | PASS | Ruff check and format check over `src`, `tests`, `scripts`, `evaluation` | Ejecutar en cada push | No localmente; sí hasta verificar CI |
| Static security analysis | PASS | Bandit over `src` with no findings | Ejecutar en CI | No localmente; sí hasta verificar CI |
| Dependency audit | PASS | pip-audit reported no known vulnerabilities at scan time | Repetir contra la base vigente en CI | No localmente; sí hasta verificar CI |
| Demo and report schema | PASS | SSH/JSONL fixtures produce AL-001, AL-003, AL-002; all locales validate against JSON Schema 2020-12 | Mantener fixtures como regresión | No |
| Controlled labeled evaluation | PASS WITH LIMITATION | 10 synthetic scenarios, 5 TP and 25 TN; precision/recall/F1 = 1.0 only for this corpus | Obtener corpus representativo sin ajustar con el conjunto final | Sí para claims de precisión |
| Package build | PASS | `python -m build --no-isolation` produced wheel and sdist; locale catalogs included | Inspeccionar artefactos en cada release | No localmente; sí para release |
| Fresh wheel install | PASS | Wheel installed into `.smoke-venv` with `--no-index --no-deps`; JSONL smoke produced 3 findings | Repetir desde clean checkout | No |
| Cross-platform CI | PENDING | Workflows cover Ubuntu/Windows/macOS and Python 3.11–3.14; no hosted run exists | Crear repo y ejecutar matriz completa | Sí |
| Secret scan | PENDING | CI pins Gitleaks v8.30.1 and verifies checksum; local binary download was blocked by session approval limit | Ejecutar Gitleaks sobre working tree e historia | Sí |
| Translation review | PENDING | Keys/placeholders/encoding technically checked; native-speaker review not claimed | Revisar copy con hablantes nativos | Sí para claim de traducción validada |
| Git repository / release | PENDING | Local Git repository initialized at `main` with a reviewed commit; no remote, tag or release exists | Add the reviewed remote, enable protections, then tag and publish only with authorization | Sí |

## Decision

Do not label AuthLens `Portfolio Ready` until the pending gates that matter for the intended audience are closed or deliberately documented: remote CI run on target platforms, a Gitleaks secret scan, review of translated copy, a representative non-synthetic evaluation and repository/release provenance. The implementation is suitable for study and local demonstration now. No remote publication or external communication was performed.

## Reproduction record

```console
python -m pytest --cov=authlens --cov-report=term-missing
python -m ruff check src tests scripts evaluation
python -m ruff format --check src tests scripts evaluation
python -m bandit -r src -q
python -m pip_audit -r requirements-dev.txt
python -m build --no-isolation
python scripts/benchmark.py
```

The latest benchmark measured 10,000 synthetic JSONL events in 1.4938 seconds with 7,780,371 traced peak bytes on this machine. It is a reproducible local measurement, not a performance promise or comparison with another product.
