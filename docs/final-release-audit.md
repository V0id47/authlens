# FINAL RELEASE AUDIT

Audit date: 2026-09-13. Scope: the published [AuthLens v0.1.0](https://github.com/V0id47/authlens/releases/tag/v0.1.0). Evidence for the source checkout, hosted workflows and downloaded release artifacts is recorded separately.

## Evidence separation

- **LOCAL EVIDENCE:** Windows 11/Python 3.12.14 validation, package inspection, clean-checkout build and wheel smoke, controlled evaluation, benchmark, Bandit, pip-audit 2.10.1 and Gitleaks 8.30.1.
- **REMOTE CI EVIDENCE:** Release commit `3f6c20cf7748cba8161443756d02cda1113bbd07`; [Lint 34742989421](https://github.com/V0id47/authlens/actions/runs/34742989421), [Test 34742989444](https://github.com/V0id47/authlens/actions/runs/34742989444), [Security 34742989428](https://github.com/V0id47/authlens/actions/runs/34742989428) and [tag build 34743002957](https://github.com/V0id47/authlens/actions/runs/34743002957) completed successfully.
- **SECURITY SCAN EVIDENCE:** Bandit and pip-audit passed locally and remotely. Gitleaks scanned the local tree, the complete local history, the hosted tree and the full fetched Git history with no undisclosed findings.
- **RELEASE EVIDENCE:** `v0.1.0` points to `3f6c20c`; the GitHub Release includes the wheel, sdist and `SHA256SUMS`. Files downloaded from the public Release matched the checksums and the wheel passed a fresh no-index installation plus CLI/demo smoke checks.

## Tests and coverage

PASS. The complete local suite reports **91 passed, 1 skipped** with **93.61%** branch-aware coverage. The skip is the Windows symlink fixture when the host cannot create symlinks. Hosted CI completed **12/12** matrix jobs on Ubuntu, Windows and macOS with Python 3.11, 3.12, 3.13 and 3.14. The Ubuntu/Python 3.12 job collected and passed all **92** tests, confirming the symlink path without a skip. Each matrix job also built the distributions and installed the wheel into an isolated environment for CLI smoke checks.

## Static and dependency analysis

PASS. Ruff check and format check cover `src`, `tests`, `scripts` and `evaluation`. Bandit covers `src`. pip-audit 2.10.1 reported no known vulnerabilities in `requirements-dev.txt` on 2026-09-13. The dependency result is time-bound to the advisory database; it is not a permanent guarantee.

## Build and packaging

PASS locally, in hosted CI and after publication. The released wheel contains the package, four locale catalogs, entry-point metadata and MIT license, and installed with `--no-index --no-deps` into a fresh environment. Help, SSH/JSONL JSON and Spanish HTML smoke runs passed. Published hashes: wheel `f9f09050337034fac01b1f857f43cbb8d6ea99300ccd149ecafc23701078f42a`; sdist `e1475558dc2a266cc3fff133336eb185ef1fc8a77c898db8ab4a3787144d9024`.

## Security review

PASS WITH DISCLOSED LIMITATIONS. Adversarial tests cover oversized values, malformed records, source mutation, symlink/non-regular input, exclusive outputs, failed finalization, closed stdout pipes, report injection, Unicode controls and raw-log minimization. The review fixed oversized SSH port conversion plus two pipe/failure-path issues.

Gitleaks 8.30.1 found three false positives in public English locale keys. The allowlist accepts only `AL-001.recommendation`, `AL-002.hypothesis` and `AL-003.hypothesis`, only in `src/authlens/locales/en.json`, against the detected secret value. After that narrow exception, both local scans and both hosted scans reported no leaks. The workflow verifies the downloaded Gitleaks checksum, fetches full history, redacts findings and uses `permissions: contents: read`.

Residual security limits remain documented: AuthLens provides investigation indicators, preserves identities and IPs in reports, cannot authenticate log provenance, and does not guarantee a fixed memory ceiling or absence of attacks. It performs no networking, login attempt, blocking action or credential verification.

## Documentation and locales

PASS WITH LIMITATION. English, Spanish, Russian and Simplified Chinese READMEs and technical documentation are present. Relative links, locale JSON, UTF-8, matching keys/placeholders, CLI help/errors, reports, fallback and OS locale mapping are technically checked. Native-speaker editorial review has not occurred and is not claimed.

## Controlled evaluation

PASS WITH LIMITATION. The evaluator uses the real parser and detector against ten synthetic scenarios. Result: **5 TP, 25 TN, 0 FP, 0 FN; precision 1.0, recall 1.0, F1 1.0** at the rule/scenario level. Thresholds were not tuned to restore these metrics. This corpus is a regression contract, not representative field validation and not evidence of production accuracy.

## Workflow and supply-chain review

PASS. Workflow permissions are read-only, third-party actions are pinned to commit SHAs with readable version comments, no `pull_request_target` is used, and the release workflow cannot publish by itself. Gitleaks binaries are version-pinned and checksum-verified. Python, build tooling, development dependencies and GitHub Actions remain part of the supply chain even though the installed runtime has no third-party package dependencies.

## Repository readiness

PASS. The exact Git root is the AuthLens directory, default branch is `main`, the repository is public at <https://github.com/V0id47/authlens>, and the release commit has green lint, security, cross-platform test and tag-build workflows. Public badges point to the real workflows and latest Release. The protected `main` branch requires a pull request, Ruff, security audit and all 12 matrix checks; force pushes and deletion remain disabled while administrator bypass remains available for recovery. Private vulnerability reporting, dependency graph, Dependabot alerts/security updates, secret scanning and push protection are enabled. Ten relevant repository topics are published.

## Decision

**PORTFOLIO READY WITH DISCLOSED LIMITATIONS.** The open limitations are synthetic evaluation only, no real-world precision/recall claim and no native-speaker editorial certification. They are stated in public documentation and block exaggerated claims, not factual portfolio publication.

The v0.1.0 release is complete. Its remaining limitations are product-validation limits stated above, not missing publication or artifact-verification steps.

## Exact final validation commands

```powershell
.venv\Scripts\python.exe -m ruff check src tests scripts evaluation
.venv\Scripts\python.exe -m ruff format --check src tests scripts evaluation
.venv\Scripts\python.exe -m pytest --cov=authlens --cov-report=term-missing --cov-report=xml -q
.venv\Scripts\python.exe -m bandit -r src -q
.venv\Scripts\python.exe -m pip_audit -r requirements-dev.txt --cache-dir .audit-cache --progress-spinner off
$gitleaks = Join-Path $env:TEMP 'authlens-gitleaks-8.30.1\bin\gitleaks.exe'
& $gitleaks dir --redact --no-banner --config .gitleaks.toml .
& $gitleaks git --redact --no-banner --config .gitleaks.toml .
.venv\Scripts\python.exe -m build --no-isolation
.venv\Scripts\python.exe evaluation\evaluate.py
.venv\Scripts\python.exe scripts\benchmark.py
```
