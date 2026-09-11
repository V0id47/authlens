import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from authlens.cli import main
from authlens.config import Settings
from authlens.errors import AuthLensError
from authlens.ingest import ingest
from authlens.parsers.ssh import parse_ssh
from authlens.safeio import new_output


def test_oversized_port_is_malformed_not_uncaught_integer_error():
    line = "2026-01-01T00:00:00Z h sshd[1]: Failed password for a from 192.0.2.1 port "
    with pytest.raises(AuthLensError, match="record"):
        parse_ssh(line + "9" * 5000, 1, Settings())


def test_failed_analysis_retains_safe_failure_log_and_removes_partial_report(tmp_path):
    source = tmp_path / "bad.jsonl"
    source.write_text("{SECRET", encoding="utf-8")
    output, log = tmp_path / "report.json", tmp_path / "run.log"
    assert (
        main(["analyze", str(source), "--strict", "--output", str(output), "--log-file", str(log)])
        == 4
    )
    assert not output.exists()
    records = [json.loads(line) for line in log.read_text().splitlines()]
    assert records[-1]["event"] == "failed" and records[-1]["code"] == "record"
    assert "SECRET" not in log.read_text()


def test_incomplete_output_removed_on_write_failure(tmp_path):
    path = tmp_path / "out"
    with pytest.raises(RuntimeError):
        with new_output(path) as stream:
            stream.write("incomplete")
            raise RuntimeError("simulated interruption")
    assert not path.exists()


def test_symlink_input_rejected_when_supported(tmp_path):
    source = tmp_path / "source"
    source.write_text("{}")
    link = tmp_path / "link"
    try:
        link.symlink_to(source)
    except OSError:
        pytest.skip("Creating symlinks requires a host privilege not available here")
    with pytest.raises(AuthLensError, match="io"):
        ingest(link, Settings())


def test_mutating_input_detected(tmp_path, monkeypatch):
    source = tmp_path / "data"
    source.write_text("{}\n", encoding="utf-8")
    import authlens.ingest as module

    original = module.parse_jsonl

    def mutate(line, number, settings):
        # A real concurrent-writer side effect, introduced at the parser boundary.
        if number == 1:
            with source.open("ab") as stream:
                stream.write(b"\n")
        return original(line, number, settings)

    monkeypatch.setattr(module, "parse_jsonl", mutate)
    with pytest.raises(AuthLensError, match="input_changed"):
        ingest(source, Settings(max_bytes=100))


def test_closed_stdout_pipe_has_defined_exit_without_shutdown_traceback(tmp_path):
    source = tmp_path / "data"
    source.write_text("{}\n")
    root = Path(__file__).resolve().parents[2]
    proc = subprocess.Popen(
        [sys.executable, "-m", "authlens", "analyze", str(source), "--format", "json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=os.environ | {"PYTHONPATH": str(root / "src")},
    )
    proc.stdout.close()
    errors = proc.stderr.read()
    proc.wait(timeout=10)
    assert proc.returncode == 3
    assert b"Exception ignored" not in errors and b"Traceback" not in errors


@pytest.mark.parametrize("args", [["--help"], ["--version"], ["analyze", "--help"]])
def test_closed_help_pipe_has_defined_exit(args):
    root = Path(__file__).resolve().parents[2]
    proc = subprocess.Popen(
        [sys.executable, "-m", "authlens", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=os.environ | {"PYTHONPATH": str(root / "src")},
    )
    proc.stdout.close()
    errors = proc.stderr.read()
    proc.wait(timeout=10)
    assert proc.returncode == 3 and b"Exception ignored" not in errors


def test_report_flush_failure_cannot_log_completed(tmp_path, monkeypatch):
    source = tmp_path / "input.jsonl"
    source.write_text("{}\n")
    output, log = tmp_path / "report", tmp_path / "run.log"
    original = os.fsync
    calls = 0

    def fail_first(descriptor):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise OSError("simulated report disk failure")
        return original(descriptor)

    monkeypatch.setattr(os, "fsync", fail_first)
    assert main(["analyze", str(source), "--output", str(output), "--log-file", str(log)]) == 3
    assert not output.exists()
    records = [json.loads(line) for line in log.read_text().splitlines()]
    assert records[-1]["event"] == "failed"
    assert "completed" not in [row["event"] for row in records]
