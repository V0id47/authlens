# Release readiness — AuthLens 0.1.0

Checked 2026-09-13. Repository: <https://github.com/V0id47/authlens>. The evidence below distinguishes local checks, hosted CI and the still-separate GitHub Release publication step. It is not a production certification or a PyPI publication claim.

| Gate | Estado | Evidencia | Limitación o siguiente acción |
|---|---|---|---|
| Product scope and threat model | PASS | Product spec, ADRs, `THREAT_MODEL.md`, `SECURITY.md`; three bounded offline rules and explicit non-goals | Mantener el alcance congelado en v0.1.0 |
| Local tests and coverage | PASS | Windows 11/Python 3.12.14: 91 passed, 1 skipped; 93.61% branch-aware coverage | El skip local requiere privilegio de symlink |
| Hosted test matrix | PASS | [Test run 34742191586](https://github.com/V0id47/authlens/actions/runs/34742191586): 12/12 jobs on Ubuntu, Windows and macOS; Python 3.11–3.14 | Hosted CI is evidence for this commit, not production deployment |
| Symlink behavior | PASS | Ubuntu/Python 3.12 job collected and passed all 92 tests; no skip | Windows local skip remains documented |
| Lint and formatting | PASS | Local Ruff checks and [Lint run 34742191573](https://github.com/V0id47/authlens/actions/runs/34742191573) | Re-run on each push |
| Static security analysis | PASS | Bandit passed locally and in hosted security CI | Static analysis has normal coverage limits |
| Dependency audit | PASS | pip-audit 2.10.1 found no known vulnerabilities locally and in CI on 2026-09-13 | Result depends on the advisory database at scan time |
| Secret scan | PASS | Gitleaks 8.30.1: local working tree and five-commit history passed; [Security run 34742191578](https://github.com/V0id47/authlens/actions/runs/34742191578) passed tree and full-history scans with redaction | Three public locale keys have exact, file-scoped false-positive exceptions |
| Controlled labeled evaluation | PASS WITH LIMITATION | 10 synthetic scenarios; 5 TP, 25 TN, 0 FP, 0 FN; precision/recall/F1 = 1.0 on that corpus | No real-world accuracy claim |
| Package build and wheel smoke | PASS | Clean-checkout wheel/sdist build, isolated no-index wheel install and CLI/demo smoke passed locally; hosted matrix also builds and smoke-installs wheels | Final release artifact hashes are recorded after the tag build |
| Locale catalogs | PASS WITH LIMITATION | en/es/ru/zh-CN JSON, keys, placeholders, UTF-8, CLI/report behavior, fallback and OS mapping are technically tested | Native-speaker editorial review not claimed |
| Public repository | PASS | Public `main` at <https://github.com/V0id47/authlens>; commit `708439b5429c0f01c33c396dc66671df62965316` produced the cited green CI runs | Branch/ruleset settings are a separate repository-administration control |
| GitHub Release | PENDING | `release.yml` is read-only and builds artifacts on `v*` tags | Create `v0.1.0`, verify its build, publish the release and install the downloaded wheel |

## Decision

The public source repository is **PORTFOLIO READY WITH DISCLOSED LIMITATIONS**. The remaining limitations are a synthetic evaluation corpus, no real-world precision/recall claim, and no native-speaker editorial certification. They prevent stronger accuracy and translation-quality claims, but do not block a factual public portfolio presentation.

The GitHub Release is still a separate gate. Do not describe v0.1.0 as released until the tag build, artifact checksums, published release and fresh install of the downloaded wheel have been verified.

## Reproduction record

```console
python -m ruff check src tests scripts evaluation
python -m ruff format --check src tests scripts evaluation
python -m pytest --cov=authlens --cov-report=term-missing --cov-report=xml
python -m bandit -r src -q
python -m pip_audit -r requirements-dev.txt
gitleaks dir --redact --no-banner --config .gitleaks.toml .
gitleaks git --redact --no-banner --config .gitleaks.toml .
python -m build --no-isolation
python evaluation/evaluate.py
python scripts/benchmark.py
```

The latest recorded benchmark measured 10,000 synthetic JSONL events in 1.4938 seconds with 7,780,371 traced peak bytes on the local machine. It is a reproducible measurement, not a performance promise or product comparison.
