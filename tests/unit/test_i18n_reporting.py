import csv
import io
import json
from datetime import UTC, datetime
from string import Formatter

import pytest
from markdown_it import MarkdownIt

from authlens.config import Settings
from authlens.engine import detect
from authlens.i18n import Translator, choose_language
from authlens.models import Dataset, Event
from authlens.reporting import make_report, render


def report_for(user="alice", lang="en"):
    events = [
        Event(
            datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC),
            "h",
            "ssh",
            user,
            "192.0.2.1",
            "failure",
            i + 1,
            f"hash:{i + 1}",
        )
        for i in range(5)
    ]
    dataset = Dataset(
        events,
        dict(
            sha256="a" * 64,
            bytes=100,
            lines=5,
            accepted=5,
            ignored=0,
            malformed=0,
            excluded=0,
            duplicates=0,
            analyzed=5,
            complete=True,
        ),
    )
    return make_report(dataset, detect(events, Settings()), Settings(), lang)


def test_catalogs_have_identical_keys_and_placeholders():
    base = Translator("en").messages
    formatter = Formatter()
    for language in ("es", "ru", "zh-CN"):
        translated = Translator(language).messages
        assert base.keys() == translated.keys()
        for key in base:
            expected = {name for _, name, _, _ in formatter.parse(base[key]) if name}
            actual = {name for _, name, _, _ in formatter.parse(translated[key]) if name}
            assert actual == expected


def test_locale_resolution(monkeypatch):
    monkeypatch.setenv("LC_ALL", "ru_RU.UTF-8")
    assert choose_language(None) == "ru"
    assert choose_language("es") == "es"
    monkeypatch.setenv("LC_ALL", "fr_FR")
    assert choose_language(None) == "en"
    monkeypatch.setenv("LC_ALL", "zh_CN.UTF-8")
    assert choose_language(None) == "zh-CN"


def test_json_preserves_evidence_and_translates_only_narrative():
    report = report_for(lang="es")
    finding = json.loads(render(report, "json", Translator("es")))["findings"][0]
    assert finding["rule_id"] == "AL-001" and finding["severity"] == "MEDIUM"
    assert finding["evidence_type"] == "DERIVED"
    assert finding["evidence"][0]["line"] == 1
    assert finding["event_count"] == 5 and finding["account_count"] == 1
    assert finding["title"] != report_for()["findings"][0]["title"]


def test_html_escapes_identity_and_has_no_script():
    output = render(report_for("<script>alert(1)</script>"), "html", Translator("en"))
    assert "<script>" not in output
    assert "&lt;script&gt;" in output
    assert "Content-Security-Policy" in output and "default-src 'none'" in output


def test_csv_neutralizes_formula_identity():
    output = render(report_for("=1+1"), "csv", Translator("en"))
    row = next(csv.DictReader(io.StringIO(output)))
    assert row["username"] == "'=1+1"
    assert json.loads(row["evidence"])[0]["line"] == 1


def test_markdown_neutralizes_html_and_links():
    output = render(report_for("[click](https://invalid.test)<b>"), "markdown", Translator("en"))
    rendered = MarkdownIt("commonmark").render(output)
    assert "<b>" not in rendered and '<a href="https://invalid.test"' not in rendered


@pytest.mark.parametrize("format", ["text", "markdown", "html", "json", "csv"])
def test_output_carries_quality_and_provenance(format):
    output = render(report_for(), format, Translator("en"))
    assert "a" * 64 in output and "AL-001" in output


def test_no_findings_report_is_explicit():
    report = report_for()
    report["findings"] = []
    assert "No indicators" in render(report, "text", Translator("en"))
    assert len(list(csv.reader(io.StringIO(render(report, "csv", Translator("en")))))) == 1
