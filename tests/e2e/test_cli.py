import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def run(*args):
    env = os.environ | {"PYTHONPATH": str(ROOT / "src"), "PYTHONIOENCODING": "utf-8"}
    return subprocess.run(
        [sys.executable, "-m", "authlens", *map(str, args)],
        capture_output=True,
        encoding="utf-8",
        env=env,
        timeout=15,
    )


@pytest.fixture
def source(tmp_path):
    path = tmp_path / "events.jsonl"
    data = [
        dict(
            timestamp=f"2026-01-01T00:00:{i:02d}Z",
            host="host",
            service="ssh",
            username="alice",
            source_ip="192.0.2.1",
            outcome="failure",
        )
        for i in range(5)
    ]
    path.write_text("\n".join(json.dumps(row) for row in data), encoding="utf-8")
    return path


@pytest.mark.parametrize("lang", ["en", "es", "ru", "zh-CN"])
def test_json_clean_and_help_localized(source, lang):
    result = run("--lang", lang, "analyze", source, "--format", "json")
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["language"] == lang and len(report["findings"]) == 1
    assert result.stderr == ""
    help_result = run("analyze", "--lang", lang, "--help")
    assert help_result.returncode == 0 and "--window-seconds" in help_result.stdout
    if lang != "en":
        assert "Show this help" not in help_result.stdout


def test_fail_on_and_partial_precedence(source):
    result = run("analyze", source, "--format", "json", "--fail-on", "MEDIUM")
    assert result.returncode == 1 and json.loads(result.stdout)["findings"]
    with source.open("a") as stream:
        stream.write("\n{BROKEN_SECRET\n")
    result = run("analyze", source, "--format", "json", "--fail-on", "MEDIUM")
    assert result.returncode == 4 and json.loads(result.stdout)["input"]["malformed"] == 1
    assert "BROKEN_SECRET" not in result.stdout + result.stderr


def test_error_is_localized_and_does_not_echo_invalid_argument(source):
    result = run("analyze", source, "--lang", "es", "--max-events", "SECRET_VALUE")
    assert result.returncode == 2
    assert "Argumentos inválidos" in result.stderr
    assert "SECRET_VALUE" not in result.stderr and not result.stdout


def test_output_and_logs_do_not_overwrite(source, tmp_path):
    output = tmp_path / "report.json"
    output.write_text("KEEP", encoding="utf-8")
    result = run("analyze", source, "--output", output)
    assert result.returncode == 3 and output.read_text() == "KEEP"
    log = tmp_path / "audit.log"
    result = run("analyze", source, "--log-file", log, "--format", "json")
    assert result.returncode == 0
    records = [json.loads(line) for line in log.read_text().splitlines()]
    assert records[-1]["event"] == "completed"
    assert "alice" not in log.read_text() and str(source) not in log.read_text()


def test_config_precedence_and_unknown_key(source, tmp_path):
    config = tmp_path / "config.toml"
    config.write_text('language="ru"\nburst_threshold=10\n', encoding="utf-8")
    result = run("--config", config, "analyze", source, "--lang", "zh-CN", "--format", "json")
    assert json.loads(result.stdout)["language"] == "zh-CN"
    assert not json.loads(result.stdout)["findings"]
    config.write_text('unknown="PRIVATE"', encoding="utf-8")
    result = run("analyze", source, "--config", config)
    assert result.returncode == 2 and "PRIVATE" not in result.stderr


@pytest.mark.parametrize("format", ["text", "json", "csv", "markdown", "html"])
def test_all_formats_written_to_new_file(source, tmp_path, format):
    output = tmp_path / ("report." + format)
    result = run("analyze", source, "--format", format, "--output", output)
    assert result.returncode == 0 and result.stdout == ""
    assert "AL-001" in output.read_text(encoding="utf-8")


def test_input_output_collision_never_touches_input(source):
    before = source.read_bytes()
    result = run("analyze", source, "--output", source)
    assert result.returncode == 3 and source.read_bytes() == before
