# Repository architecture

Planned responsibilities, with no empty placeholder subsystems:

```text
authlens/
├── .github/
│   ├── workflows/{lint,test,security,release}.yml
│   ├── ISSUE_TEMPLATE/{bug_report,feature_request}.yml
│   ├── pull_request_template.md
│   └── dependabot.yml
├── docs/
│   ├── product-specification.md
│   ├── development-phases.md
│   ├── repository-architecture.md
│   ├── research.md
│   ├── architecture.md
│   ├── installation.md
│   ├── getting-started.md
│   ├── configuration.md
│   ├── detection-logic.md
│   ├── security-model.md
│   ├── troubleshooting.md
│   ├── development.md
│   ├── portfolio.md
│   ├── release-readiness.md
│   ├── report-schema.json
│   └── adr/{0001-language,0002-evidence,0003-offline-scope}.md
├── examples/
│   ├── ssh-demo.log
│   ├── events.jsonl
│   ├── config.toml
│   └── expected-findings.json
├── scripts/benchmark.py
├── src/authlens/
│   ├── __init__.py
│   ├── __main__.py
│   ├── models.py
│   ├── errors.py
│   ├── config.py
│   ├── i18n.py
│   ├── ingest.py
│   ├── engine.py
│   ├── reporting.py
│   ├── safeio.py
│   ├── cli.py
│   ├── parsers/{__init__,jsonl,ssh,common}.py
│   └── locales/{en,es,ru,zh-CN}.json
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── regression/
│   └── e2e/
├── .gitignore
├── pyproject.toml
├── requirements-dev.txt
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── README.md
├── README.es.md
├── README.ru.md
├── README.zh-CN.md
├── THREAT_MODEL.md
└── SECURITY.md
```

Keep parsers separate because each input has a different grammar. Keep one detection module until rule complexity justifies splitting. Put catalogs inside package resources so wheels work outside the source tree. No generic `utils`, plugin framework, server or integration folders without an implemented responsibility.
