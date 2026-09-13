# v0.1.0 repository and release record

Completed on 2026-09-13. Evidence and exact run links are recorded in [release-readiness.md](release-readiness.md).

## Before repository creation

- [x] Selected `authlens`, public visibility and the repository owner.
- [x] Reviewed [SECURITY.md](../SECURITY.md), [THREAT_MODEL.md](../THREAT_MODEL.md) and the [release-readiness record](release-readiness.md).
- [x] Recorded the implementation lessons and detection limits in [portfolio.md](portfolio.md).
- [x] Disclosed that translated documentation received technical checks without native-speaker editorial certification.
- [x] Reviewed tracked files for credentials, tokens, personal paths and private infrastructure details.
- [x] Kept documentation IPs (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`) clearly synthetic.

## Before first push

- [x] Initialized Git in the AuthLens project directory only.
- [x] Inspected tracked and ignored files before publication.
- [x] Scanned the complete working tree and Git history with Gitleaks 8.30.1.
- [x] Confirmed `.gitignore` excludes local environments, caches, coverage, reports, logs and build output while retaining the synthetic SSH fixture.
- [x] Confirmed no `.env`, shell history, editor state or absolute personal path is tracked.
- [x] Inspected `MANIFEST.in`, wheel and sdist inventories; no local report, credential or temporary file ships.
- [x] Created the initial AuthLens v0.1.0 source commit and preserved the repository history.

## After CI is enabled

- [x] Confirmed Ruff check and format in the hosted lint workflow.
- [x] Passed the 12-job test matrix on Ubuntu, Windows and macOS with Python 3.11–3.14.
- [x] Confirmed locale package data and isolated-wheel smoke installation across the matrix.
- [x] Passed Bandit, pip-audit and working-tree/full-history Gitleaks scans.
- [x] Confirmed artifact retention and read-only workflow permissions.
- [x] Added badges and links backed by completed GitHub Actions runs.

## Before tagging `v0.1.0`

- [x] Ran the validation commands in [release-readiness.md](release-readiness.md), including clean-checkout artifact checks.
- [x] Confirmed version agreement in `pyproject.toml`, `src/authlens/__init__.py`, changelog and package metadata.
- [x] Disclosed the synthetic-only evaluation and absence of native-speaker editorial certification.
- [x] Reviewed release notes to remove unsupported production, accuracy, enterprise and adoption claims.
- [x] Built and inspected the wheel, sdist, checksums and archive contents.
- [x] Confirmed tag `v0.1.0` matches package version `0.1.0` and release commit `3f6c20c`.

## After release

- [x] Downloaded the public Release assets and matched the published SHA-256 checksums.
- [x] Installed the released wheel with `--no-index --no-deps` in a fresh environment and reran CLI/demo smoke checks.
- [x] Recorded the Release URL, CI run IDs, scan versions and local Windows symlink skip in [release-readiness.md](release-readiness.md).
- [x] Enabled private vulnerability reporting, dependency monitoring and automated security updates.
- [x] Protected `main` with pull requests and all 14 hosted CI checks; kept force pushes and deletion disabled.
- [x] Published ten relevant repository topics.
- [ ] Monitor reports through the private vulnerability-reporting channel.
- [ ] Publish a patch release only for a verified defect that warrants one.

## Draft release notes

AuthLens v0.1.0 is an offline authentication triage CLI. It accepts a documented SSH grammar or strict JSONL, correlates three explainable patterns, preserves source provenance and exports localized reports. The release is bounded, does not make network connections or authentication attempts, and does not prove compromise. See limitations and verification status before using the output operationally.
