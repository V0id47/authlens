# Release readiness — AuthLens 0.1.0

Checked 2026-09-13. Repository: <https://github.com/V0id47/authlens>. Release: <https://github.com/V0id47/authlens/releases/tag/v0.1.0>. The evidence below distinguishes local checks, hosted CI and released-artifact verification. It is not a production certification or a PyPI publication claim.

| Gate | Estado | Evidencia | Limitación o siguiente acción |
|---|---|---|---|
| Product scope and threat model | PASS | Product spec, ADRs, `THREAT_MODEL.md`, `SECURITY.md`; three bounded offline rules and explicit non-goals | Mantener el alcance congelado en v0.1.0 |
| Local tests and coverage | PASS | Windows 11/Python 3.12.14: 91 passed, 1 skipped; 93.61% branch-aware coverage | El skip local requiere privilegio de symlink |
| Hosted test matrix | PASS | [Test run 34742989444](https://github.com/V0id47/authlens/actions/runs/34742989444): 12/12 jobs on Ubuntu, Windows and macOS; Python 3.11–3.14 | Hosted CI is evidence for this commit, not production deployment |
| Symlink behavior | PASS | Ubuntu/Python 3.12 job collected and passed all 92 tests; no skip | Windows local skip remains documented |
| Lint and formatting | PASS | Local Ruff checks and [Lint run 34742989421](https://github.com/V0id47/authlens/actions/runs/34742989421) | Re-run on each push |
| Static security analysis | PASS | Bandit passed locally and in hosted security CI | Static analysis has normal coverage limits |
| Dependency audit | PASS | pip-audit 2.10.1 found no known vulnerabilities locally and in CI on 2026-09-13 | Result depends on the advisory database at scan time |
| Secret scan | PASS | Gitleaks 8.30.1: local working tree and complete Git history passed; [Security run 34742989428](https://github.com/V0id47/authlens/actions/runs/34742989428) passed tree and full-history scans with redaction | Three public locale keys have exact, file-scoped false-positive exceptions |
| Controlled labeled evaluation | PASS WITH LIMITATION | 10 synthetic scenarios; 5 TP, 25 TN, 0 FP, 0 FN; precision/recall/F1 = 1.0 on that corpus | No real-world accuracy claim |
| Package build and wheel smoke | PASS | [Tag build 34743002957](https://github.com/V0id47/authlens/actions/runs/34743002957) passed; the published wheel installed with `--no-index --no-deps` in a fresh environment and passed help, SSH, JSONL and Spanish HTML smoke checks | Wheel SHA-256 `f9f09050337034fac01b1f857f43cbb8d6ea99300ccd149ecafc23701078f42a`; sdist SHA-256 `e1475558dc2a266cc3fff133336eb185ef1fc8a77c898db8ab4a3787144d9024` |
| Locale catalogs | PASS WITH LIMITATION | en/es/ru/zh-CN JSON, keys, placeholders, UTF-8, CLI/report behavior, fallback and OS mapping are technically tested | Native-speaker editorial review not claimed |
| Public repository | PASS | Public `main` at <https://github.com/V0id47/authlens>; release commit `3f6c20cf7748cba8161443756d02cda1113bbd07` produced the cited green CI runs; ten relevant repository topics are published | Repository popularity or adoption is not claimed |
| Repository administration | PASS | `main` requires a pull request plus Ruff, security audit and all 12 matrix jobs; force pushes and deletion remain disabled; administrators retain bypass access for recovery | Changes to the workflow job names require the protected checks to be updated |
| Hosted security controls | PASS | Private vulnerability reporting, dependency graph, Dependabot alerts, security updates and grouped security updates are enabled; secret scanning and push protection remain enabled | Dependabot findings are time-bound to GitHub's advisory data |
| GitHub Release | PASS | [AuthLens v0.1.0](https://github.com/V0id47/authlens/releases/tag/v0.1.0) points to `3f6c20c` and includes wheel, sdist and `SHA256SUMS`; all three were downloaded and verified | GitHub also supplies automatic source archives |

## Decision

The public source repository is **PORTFOLIO READY WITH DISCLOSED LIMITATIONS**. The remaining limitations are a synthetic evaluation corpus, no real-world precision/recall claim, and no native-speaker editorial certification. They prevent stronger accuracy and translation-quality claims, but do not block a factual public portfolio presentation.

AuthLens v0.1.0 is publicly released. The tag build, published checksums and a fresh installation of the downloaded wheel were verified before this record was finalized.

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
