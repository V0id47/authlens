import json
from pathlib import Path

import jsonschema
import pytest

from authlens.config import Settings
from authlens.engine import detect
from authlens.ingest import ingest
from authlens.reporting import make_report

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("format,name", [("ssh", "ssh-demo.log"), ("jsonl", "events.jsonl")])
def test_demo_matches_independent_fixture_contract_and_schema(format, name):
    settings = Settings(input_format=format)
    data = ingest(ROOT / "examples" / name, settings)
    findings = detect(data.events, settings)
    expected = json.loads((ROOT / "examples/expected-findings.json").read_text())
    actual = [
        {key: getattr(f, key) for key in ("rule_id", "severity", "event_count", "account_count")}
        for f in findings
    ]
    assert actual == expected
    assert data.summary["complete"] and data.summary["analyzed"] == 12
    for language in ("en", "es", "ru", "zh-CN"):
        report = make_report(data, findings, settings, language)
        # Serialization turns tuple settings into their public JSON array representation.
        report = json.loads(json.dumps(report))
        schema = json.loads((ROOT / "docs/report-schema.json").read_text())
        jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(
            report
        )
