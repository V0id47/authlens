# FINAL RELEASE AUDIT

Audit date: 2026-09-11. Scope: AuthLens v0.1.0 local release candidate. This audit uses the files in this directory, fresh local commands and recorded audit evidence. It does not treat a workflow definition as a successful remote run.

## Evidence separation

- **LOCAL EVIDENCE:** Windows 11/Python 3.12.14 validation, local package inventories, local scans, local benchmark and the reviewed Git commit.
- **REMOTE CI EVIDENCE:** None. The workflows are prepared but no hosted runner has executed them.
- **SECURITY SCAN EVIDENCE:** Bandit and the recorded authorized pip-audit run passed; Gitleaks remains pending because the local binary could not be obtained in this session.
- **RELEASE EVIDENCE:** A reviewed local `main` commit exists; no remote, tag or GitHub Release exists. A separate clean checkout was built and its wheel was installed and exercised locally.

## Tests

PASS. The complete suite reports **91 passed, 1 skipped**. The skip is the Windows symlink fixture when the host cannot create symlinks; the test records that limitation. Unit, integration, regression, adversarial and subprocess e2e tests all run against real parser, detector, exporters and CLI boundaries.

Command:

```powershell
.venv\Scripts\python.exe -m pytest --cov=authlens --cov-report=term-missing --cov-report=xml -q
```

## Coverage

PASS. Branch-aware coverage is **93.61%**, above the configured 80% gate. Subprocess coverage is enabled in `pyproject.toml`. Coverage measures exercised implementation paths; it does not establish field precision, recall or safe autonomous response.

## Static analysis

PASS locally. Ruff check and format check over `src`, `tests`, `scripts` and `evaluation`, plus Bandit over `src`, completed without findings.

```powershell
.venv\Scripts\python.exe -m ruff check src tests scripts evaluation
.venv\Scripts\python.exe -m ruff format --check src tests scripts evaluation
.venv\Scripts\python.exe -m bandit -r src -q
```

## Dependency audit

PASS at audit time. An authorized run of `pip-audit -r requirements-dev.txt` reported no known vulnerabilities. A later sandbox rerun could not upgrade its temporary pip tooling because network access is restricted; that is an environment limitation, not a clean second scan. This result depends on the vulnerability database date and does not remove the need for future updates.

```powershell
.venv\Scripts\python.exe -m pip_audit -r requirements-dev.txt --cache-dir .audit-cache --progress-spinner off
```

## Build

PASS locally. `python -m build --no-isolation` produced `dist/authlens-0.1.0-py3-none-any.whl` and `dist/authlens-0.1.0.tar.gz`, and the same build completed from a clean checkout of the reviewed commit. The sdist includes source, docs, examples and tests by design; local caches are excluded.

```powershell
.venv\Scripts\python.exe -m build --no-isolation
```

## Packaging

PASS locally. The wheel inventory contains the `authlens` package, four locale JSON catalogs, entry point metadata and the MIT license. A wheel built from a separate clean checkout installed into `.smoke-venv` with `--no-index --no-deps`; help, SSH JSON, JSONL JSON and Spanish HTML smoke runs passed. Compute and publish SHA-256 values from the final release files; no GitHub artifact exists yet.

The JSON schema is shipped in the source distribution/docs and used by the evaluation tests; runtime reporting does not read it from disk.

## Security

PASS WITH LIMITATION. Adversarial tests cover oversized ports, malformed records, source mutation, symlink/non-regular input, exclusive outputs, failed finalization, closed stdout pipes, HTML/Markdown/CSV injection, Unicode controls and raw-log minimization. The independent review found and the implementation fixed two pipe/failure-path bugs plus oversized integer conversion. No network, authentication attempt, blocking action or dynamic loading exists.

Gitleaks is **PENDING REMOTE CI**. `.github/workflows/security.yml` pins Gitleaks v8.30.1, verifies the published checksum, uses read-only workflow permissions and scans the complete working tree with redaction. A local binary download was blocked by the session approval limit; no local Gitleaks pass is claimed.

## Documentation

PASS WITH LIMITATION. English, Spanish, Russian and Simplified Chinese READMEs, product specification, architecture, configuration, detection logic, security model, troubleshooting, development, threat model, ADRs, contribution policy, changelog, portfolio statement, interview review, release checklist and this audit are present. Relative links were checked across the public documentation set. The technical i18n review confirms matching keys/placeholders and valid UTF-8/JSON. Native-speaker review remains pending.

## Cross-platform

PASS WITH LIMITATION. Workflows declare Ubuntu, Windows and macOS with Python 3.11–3.14 and cover lint, tests, coverage, build, wheel smoke install, Bandit, pip-audit and artifacts. No hosted runner has executed because this directory is not connected to a remote Git repository. Windows/Python 3.12 is the only local runtime evidence.

## Translation

PASS WITH LIMITATION. All four catalogs have identical keys and formatting placeholders; locale detection, fallback, CLI help/errors and report narratives are tested. Unicode catalog parsing passed. A native-speaker editorial review has not occurred and must not be claimed.

## Representative dataset

PASS WITH LIMITATION. `evaluation/events.jsonl` and `evaluation/labels.json` contain ten controlled scenarios: normal success, exact and outside boundaries, multi-account breadth, below-threshold breadth, success ordering, host/service separation and duplicate handling. The evaluator reports **5 TP, 25 TN, 0 FP, 0 FN; precision 1.0, recall 1.0, F1 1.0** at the behavioral rule/scenario level. This is a synthetic regression corpus, not a real-world validation set and not evidence of production accuracy. No tuning set was used; thresholds remain specified by the product design.

```powershell
.venv\Scripts\python.exe evaluation\evaluate.py
```

## Repository readiness

PENDING. A local Git repository now exists at the AuthLens project root, on `main`, with a reviewed commit. No remote was initialized or contacted. Before the first push, follow [release-checklist.md](release-checklist.md), inspect the complete working tree, run Gitleaks, remove local artifacts, configure branch protection/CI and then record the resulting remote evidence. Do not add public badges before a successful workflow run.

## Remaining blockers

The correct decision is **NOT PORTFOLIO READY** because important external gates remain open: remote CI, remote/verified secret scanning, native-speaker translation review, representative non-synthetic evaluation, and GitHub repository/release provenance. The codebase is ready for personal study and a local demo. Do not start SentinelHTTP until these gates are consciously closed or the project is explicitly labeled a limited local portfolio artifact.

## Exact final validation commands

```powershell
# Run the following from the AuthLens project root.
.venv\Scripts\python.exe -m ruff check src tests scripts evaluation
.venv\Scripts\python.exe -m ruff format --check src tests scripts evaluation
.venv\Scripts\python.exe -m pytest --cov=authlens --cov-report=term-missing --cov-report=xml -q
.venv\Scripts\python.exe -m bandit -r src -q
.venv\Scripts\python.exe -m pip_audit -r requirements-dev.txt --cache-dir .audit-cache --progress-spinner off
.venv\Scripts\python.exe -m build --no-isolation
uv --cache-dir .uv-cache pip install --python .smoke-venv\Scripts\python.exe --no-index --no-deps --force-reinstall dist\authlens-0.1.0-py3-none-any.whl
.smoke-venv\Scripts\python.exe -m authlens analyze examples\events.jsonl --lang zh-CN --format json
.venv\Scripts\python.exe evaluation\evaluate.py
.venv\Scripts\python.exe scripts\benchmark.py
```

The first push checklist adds the Gitleaks command and a complete history scan after repository initialization. Keep all output artifacts private during validation.
