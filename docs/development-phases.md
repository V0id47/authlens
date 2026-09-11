# Development phases and acceptance

Plan date: 2026-09-11. Authority: [product specification](product-specification.md). This plan uses in-session execution for the tightly coupled core; independent review can use a reviewer. New standalone directory, no existing Git repository or baseline tests. No remote operations. Unit tests precede behavior; phases 6 and 7 are completion gates, not permission to postpone i18n/testing.

## Global constraints

Python 3.11+, runtime standard library only; locales en/es/ru/zh-CN; offline regular-file analysis; no raw lines in output; v0.1.0; schema 1.0. No claim of production readiness or CI success without evidence.

| Phase | Deliverable / files | Concrete acceptance |
|---|---|---|
| 0 Design | portfolio roadmap, product spec, repository tree, ADRs, threat model | Selected single project; rules, scope, limits, evidence, test oracle and exit semantics specified |
| 1 Foundation | pyproject.toml, models.py, errors.py, config.py, i18n.py, locales | Import/install succeeds; bad TOML, bool-as-int, unknown keys and unsupported language rejected; four matching catalogs |
| 2 Core Engine | parsers/, ingest.py, safeio.py | SSH + JSONL normalize to UTC; data quality balances; exact source hash; hard limits stop; duplicate/exclusion counters explicit |
| 3 Detection | engine.py, tests/unit/test_engine.py | AL-001/002/003 positive/negative/boundary cases and randomized independent oracle pass; source/host/service separated |
| 4 Reporting | reporting.py, docs/report-schema.json | All 5 formats preserve evidence/quality; hostile identity never creates HTML/Markdown active content or CSV formula |
| 5 CLI | cli.py, __main__.py, tests/e2e | Entrypoint and flags work; stdout parseable; distinct codes; exclusive output/log create and correct diagnostic stream |
| 6 i18n | locales/*.json, translated READMEs | Help, errors and narratives localized; keys/placeholders match; language precedence and fallback tested |
| 7 Testing | tests/unit, integration, regression, e2e | Whole suite passes; >80% coverage goal assessed; wheel fresh-install demo and malformed-input scenarios run |
| 8 Hardening | THREAT_MODEL, SECURITY, security CI | No raw secrets in logs/reports; bounded memory/input; injection regressions; static and dependency checks run or explicitly pending |
| 9 Documentation | README ×4, docs/, examples/ | Actual runnable commands, sample output, limitations, severity rationale, contribution instructions and honest portfolio statement |
| 10 Release | workflows, changelog, license, build artifacts, release-readiness.md | Local distributions built and installed; remote CI/publication status explicitly recorded; no premature Portfolio Ready label |

## Task execution sequence

- [x] T0: Write and self-review design documents before production code. Check no contradictory field names, hidden networking or unspecific detectors.
- [x] T1: Write tests for `Settings.from_mapping`, `parse_jsonl`, `parse_ssh` and catalog fallback. Run failing tests, implement models/config/parsers/i18n, rerun. Test: naïve timestamp rejected; `2026-01-01T01:00:00+01:00` becomes UTC midnight; non-string outcome fails; traditional log without year fails.
- [x] T2: Write ingestion tests on tmp files: one valid, one malformed, one duplicate, one ignored; assert counters and hash. Implement `ingest(path, settings) -> Dataset`; test 16-byte line cap, file cap, symlink/non-regular rejection and source mutation detection. No full path/raw record in errors.
- [x] T3: Write detector tests with manually specified events at seconds 0,1,2,3,300 and success 301. Assert inclusive edge and correct account/source grouping; implement `detect(events, settings) -> list[Finding]`. Add randomized O(n²) test oracle before changing correlation optimizations.
- [x] T4: Write renderer tests with identity `<script>alert(1)</script>` and `=1+1`; implement `make_report(dataset, findings, settings, language)` and `render(report, format, translator) -> str`. Check event evidence, CSV quoting and escaping, no raw suffix.
- [x] T5: Write subprocess tests for `authlens analyze`, clean JSON, malformed input code 4, invalid config code 2, output exists code 3 and fail-on code 1. Implement CLI orchestration and safe output/log handling. Run all formats/locales.
- [x] T6: Complete README translations and technical docs against actual behavior; create synthetic demo and expected findings. Verify demo produces three indicators and no external activity.
- [x] T7: Run lint, format, tests/coverage, build, fresh wheel install, static analysis and dependency audit. Investigate failures with minimal regressions. Run independent security/correctness review; fix important findings. Record actual results and external gates in release-readiness.md. Remote CI, local Gitleaks and native-speaker review remain explicitly pending gates.

Interfaces: `Settings` is immutable; `Dataset` holds events, summary, diagnostics; `Finding` holds IDs and evidence references; only reporting turns codes into localized prose. CLI constructs settings once. Config, parsing and rendering errors use `AuthLensError(code)` with no raw input interpolation.
