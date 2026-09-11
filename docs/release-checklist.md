# First repository and release checklist

This checklist prepares a repository. It does not publish, push, tag or create a release automatically.

## Before repository creation

- [ ] Choose the final GitHub repository name and confirm it is available.
- [ ] Decide visibility and add the repository owner/maintainer.
- [ ] Read [SECURITY.md](../SECURITY.md), [THREAT_MODEL.md](../THREAT_MODEL.md) and the [release-readiness record](release-readiness.md).
- [ ] Replace any personal placeholder text in `docs/portfolio.md` with the owner's own learning notes.
- [ ] Decide whether translated READMEs receive native-speaker review; record that honestly.
- [ ] Review all files for real credentials, tokens, API keys, personal paths, usernames and private infrastructure details.
- [ ] Keep documentation IPs (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`) clearly synthetic.

## Before first push

- [ ] Initialize the repository in this project directory only; do not initialize the parent knowledge base by accident.
- [ ] Check `git status --short --ignored` and inspect every non-ignored file.
- [ ] Run Gitleaks on the complete working tree, including history if any history was imported.
- [ ] Confirm `.gitignore` excludes virtual environments, caches, coverage, reports, logs and build output while retaining the SSH demo fixture.
- [ ] Confirm no `.env`, shell history, editor state or absolute personal path is tracked.
- [ ] Review `MANIFEST.in`, wheel and sdist inventories; no local reports, credentials or temporary files may ship.
- [ ] Make the initial commit with a factual message such as `feat: add AuthLens 0.1.0 release candidate`.

## After CI is enabled

- [ ] Run the lint workflow and confirm Ruff check/format pass.
- [ ] Run the test matrix on Ubuntu, Windows and macOS for Python 3.11–3.14.
- [ ] Confirm locale package data and wheel smoke installation pass on every matrix job.
- [ ] Confirm Bandit, pip-audit and Gitleaks jobs pass; inspect warnings rather than ignoring them.
- [ ] Confirm artifact retention and minimal workflow permissions.
- [ ] Add only verified CI links/badges to READMEs. A workflow file alone is not evidence of a passing run.

## Before tagging `v0.1.0`

- [ ] Re-run the local commands in `docs/release-readiness.md` from a clean checkout.
- [ ] Confirm version agreement in `pyproject.toml`, `src/authlens/__init__.py`, changelog and package metadata.
- [ ] Complete or explicitly disclose native-speaker review and representative labeled evaluation.
- [ ] Review release notes for unsupported claims: no production, accuracy, enterprise or public-user claims without evidence.
- [ ] Build wheel/sdist and inspect checksums and contents.
- [ ] Confirm the tag exactly matches the package version.

## After release

- [ ] Verify the hosting platform's release assets and checksums from a clean environment.
- [ ] Install the released wheel with `--no-index --no-deps` where appropriate and rerun the demo.
- [ ] Record the release URL, CI run IDs, scan versions and any skipped tests in `docs/release-readiness.md`.
- [ ] Monitor security reports through the private channel described in `SECURITY.md`.
- [ ] Plan a patch release for verified bugs only; do not use a release to smuggle in new v0.1.0 features.

## Draft release notes

AuthLens v0.1.0 is an offline authentication triage CLI. It accepts a documented SSH grammar or strict JSONL, correlates three explainable patterns, preserves source provenance and exports localized reports. The release is bounded, does not make network connections or authentication attempts, and does not prove compromise. See limitations and verification status before using the output operationally.
