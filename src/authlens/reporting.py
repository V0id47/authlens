"""Localized, escaped reports over one authoritative JSON-compatible model."""

import csv
import html
import io
import json
import re
from dataclasses import asdict
from datetime import UTC, datetime

from authlens import __version__
from authlens.config import Settings
from authlens.i18n import Translator
from authlens.models import Dataset, Finding


def make_report(
    dataset: Dataset, findings: list[Finding], settings: Settings, language: str
) -> dict:
    translate = Translator(language)
    output = []
    for finding in findings:
        item = asdict(finding)
        item["start"] = finding.start.isoformat()
        item["end"] = finding.end.isoformat()
        item["evidence"] = [
            asdict(event) | {"timestamp": event.timestamp.isoformat()} for event in finding.evidence
        ]
        item.update(rule_version="1", evidence_type="DERIVED", classification="indicator")
        for name in ("title", "inference", "hypothesis", "recommendation", "false_positive"):
            item[name] = translate(f"{finding.rule_id}.{name}")
        item["observation"] = translate(
            "observation_text",
            events=finding.event_count,
            accounts=finding.account_count,
            start=item["start"],
            end=item["end"],
        )
        technique = "T1110/003" if finding.rule_id == "AL-002" else "T1110/001"
        item["references"] = [f"https://attack.mitre.org/techniques/{technique}/"]
        threshold = {
            "AL-001": settings.burst_threshold,
            "AL-002": settings.spray_threshold,
            "AL-003": settings.success_threshold,
        }[finding.rule_id]
        item["parameters"] = {"window_seconds": settings.window_seconds, "threshold": threshold}
        output.append(item)
    return {
        "schema_version": "1.0",
        "tool": "AuthLens",
        "version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "language": language,
        "notice": translate("report_notice"),
        "input": dataset.summary,
        "diagnostics": dataset.diagnostics,
        "settings": asdict(settings),
        "findings": output,
    }


def _json(value, pretty=False):
    return json.dumps(value, ensure_ascii=False, indent=2 if pretty else None, allow_nan=False)


def _csv_cell(value):
    text = str(value)
    if text.lstrip().startswith(("=", "+", "-", "@")) or text.startswith(("\t", "\r", "\n")):
        return "'" + text
    return text


def _csv(report):
    buffer = io.StringIO(newline="")
    fields = [
        "schema_version",
        "version",
        "generated_at",
        "sha256",
        "complete",
        "input_quality",
        "settings",
        "finding_id",
        "rule_id",
        "rule_version",
        "severity",
        "confidence",
        "evidence_type",
        "classification",
        "host",
        "service",
        "source_ip",
        "username",
        "start",
        "end",
        "event_count",
        "account_count",
        "title",
        "observation",
        "inference",
        "hypothesis",
        "recommendation",
        "false_positive",
        "evidence_truncated",
        "evidence",
        "references",
    ]
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for finding in report["findings"]:
        row = {key: finding.get(key, "") for key in fields}
        row.update(
            schema_version=report["schema_version"],
            version=report["version"],
            generated_at=report["generated_at"],
            sha256=report["input"]["sha256"],
            complete=report["input"]["complete"],
            input_quality=_json(report["input"]),
            settings=_json(report["settings"]),
            evidence=_json(finding["evidence"]),
            references=_json(finding["references"]),
        )
        writer.writerow(
            {key: _csv_cell("" if value is None else value) for key, value in row.items()}
        )
    return buffer.getvalue()


def _md(value):
    escaped = html.escape(str(value), quote=True)
    return re.sub(r"([\\`*_{}\[\]()#+.!|~-])", r"\\\1", escaped)


def _metadata(report):
    return {key: value for key, value in report.items() if key not in ("findings", "notice")}


def _narratives(finding):
    return (
        (key, finding[key])
        for key in ("observation", "inference", "hypothesis", "recommendation", "false_positive")
    )


def _text(report, tr):
    lines = [
        tr("report_title"),
        report["notice"],
        "",
        tr("provenance"),
        _json(_metadata(report), pretty=True),
        "",
        tr("findings"),
    ]
    if not report["findings"]:
        lines.append(tr("no_findings"))
    for finding in report["findings"]:
        lines.append(f"\n[{finding['severity']}] {finding['rule_id']} — {finding['title']}")
        for key, value in _narratives(finding):
            lines.append(f"{tr(key)}: {value}")
        lines.append(tr("evidence") + ": " + _json(finding, pretty=True))
    return "\n".join(lines) + "\n"


def _markdown(report, tr):
    lines = [
        "# " + _md(tr("report_title")),
        "",
        _md(report["notice"]),
        "",
        "## " + _md(tr("provenance")),
        "",
        "<pre>" + html.escape(_json(_metadata(report), pretty=True)) + "</pre>",
        "",
        "## " + _md(tr("findings")),
        "",
    ]
    if not report["findings"]:
        lines.append(_md(tr("no_findings")))
    for finding in report["findings"]:
        lines.extend(
            ["### " + _md(f"{finding['rule_id']} · {finding['severity']} · {finding['title']}"), ""]
        )
        for key, value in _narratives(finding):
            lines.extend([f"**{_md(tr(key))}:** {_md(value)}", ""])
        lines.extend(["<pre>" + html.escape(_json(finding, pretty=True)) + "</pre>", ""])
    return "\n".join(lines) + "\n"


def _html(report, tr):
    escape = html.escape
    parts = [
        f'<!doctype html><html lang="{escape(tr.language)}"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; '
        "style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'\">",
        f"<title>{escape(tr('report_title'))}</title>",
        "<style>body{margin:0;background:#f3f5f6;color:#182c3b;font:16px/1.6 system-ui,sans-serif}"
        "main{max-width:1000px;margin:auto;padding:40px 24px}header{border-top:6px solid #17666b}"
        "h1{font-size:2.2rem;line-height:1.15}h2{margin-top:2rem}article{background:white;"
        "border:1px solid #cbd5dc;border-left:5px solid #a96516;margin:24px 0;padding:24px}"
        "pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#e9eef1;padding:16px;"
        "font-size:.8rem}summary{cursor:pointer;font-weight:600}p{overflow-wrap:anywhere}"
        "@media print{body{background:white}main{padding:0}details{display:block}}"
        "</style></head><body><main><header><p>AuthLens · " + escape(report["version"]) + "</p>",
        f"<h1>{escape(tr('report_title'))}</h1><p>{escape(report['notice'])}</p></header>",
        f"<h2>{escape(tr('provenance'))}</h2><pre>{escape(_json(_metadata(report), True))}</pre>",
        f"<h2>{escape(tr('findings'))} · {len(report['findings'])}</h2>",
    ]
    if not report["findings"]:
        parts.append(f"<p>{escape(tr('no_findings'))}</p>")
    for finding in report["findings"]:
        parts.append(
            f"<article><p>{escape(finding['rule_id'])} · {escape(finding['severity'])} · "
            f"{escape(finding['confidence'])}</p><h3>{escape(finding['title'])}</h3>"
        )
        for key, value in _narratives(finding):
            parts.append(f"<p><strong>{escape(tr(key))}</strong><br>{escape(value)}</p>")
        parts.append(
            f"<details><summary>{escape(tr('evidence'))}</summary>"
            f"<pre>{escape(_json(finding, True))}</pre></details></article>"
        )
    parts.append("</main></body></html>\n")
    return "".join(parts)


def render(report: dict, format: str, translator: Translator) -> str:
    if format == "json":
        return _json(report, pretty=True) + "\n"
    if format == "csv":
        return _csv(report)
    return {"text": _text, "markdown": _markdown, "html": _html}[format](report, translator)
