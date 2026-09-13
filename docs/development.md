# Development and verification

Install `requirements-dev.txt`, then editable package. This is a pinned development snapshot, not runtime requirements. Run `python -m ruff check src tests scripts evaluation`, `python -m ruff format --check src tests scripts evaluation`, `python -m pytest --cov=authlens --cov-report=term-missing`, `python -m bandit -r src -q`, `python -m pip_audit -r requirements-dev.txt`, and `python -m build`.

Tests live in unit/integration/regression/e2e. The correlation oracle deliberately uses a slower independent implementation in tests. Real filesystem and subprocess tests protect install/CLI behavior; mocks are restricted to difficult failures such as disk flush errors and a deterministic concurrent-writer side effect. Coverage includes subprocesses using coverage.py's subprocess patch. Symlink creation may require privilege on Windows; that test explicitly skips when unavailable. Hosted Ubuntu CI exercises it and passes all 92 tests.

`python scripts/benchmark.py` measures a deterministic synthetic 10k-event end-to-end workload using wall clock and tracemalloc, outputs machine-readable metrics and does not promise an SLA. It creates data only in a temporary directory and cleans it up. Compare on the same machine/runtime and consider report serialization amplification.

CI definitions cover lint/format, Python 3.11–3.14 on three OSes, wheel/source build and isolated-wheel smoke, Bandit, dependency and secret scans. A workflow file is not proof it passed. `release.yml` builds downloadable artifacts on a tag/manual run and has no publish permission. The v0.1.0 GitHub Release was published separately after its tag build and checks completed.

The [interview review](interview-review.md) connects each implementation area to concrete checks: module tracing, threshold changes, inclusive-window boundaries, source-line evidence and released-wheel smoke tests. [Portfolio notes](portfolio.md) summarize the resulting engineering lessons and documented limits.
