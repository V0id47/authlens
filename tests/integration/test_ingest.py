import hashlib
import json

import pytest

from authlens.config import Settings
from authlens.errors import AuthLensError
from authlens.ingest import ingest


def write_events(path, count=1):
    rows = [
        json.dumps(
            dict(
                timestamp=f"2026-01-01T00:00:{i:02d}Z",
                host="lab",
                service="ssh",
                username="alice",
                source_ip="192.0.2.1",
                outcome="failure",
            )
        )
        for i in range(count)
    ]
    path.write_text("\n".join(rows), encoding="utf-8")
    return path


def test_quality_hash_and_duplicate_provenance(tmp_path):
    path = write_events(tmp_path / "events")
    line = path.read_bytes()
    raw = line + b"\n" + line + b"\n\n{bad\n"
    path.write_bytes(raw)
    data = ingest(path, Settings())
    assert data.summary["sha256"] == hashlib.sha256(raw).hexdigest()
    assert data.summary["lines"] == 4
    assert data.summary["accepted"] == 2
    assert data.summary["duplicates"] == 1
    assert data.summary["malformed"] == 1
    assert data.summary["ignored"] == 1
    assert data.summary["complete"] is False
    assert len(data.events) == 1 and data.events[0].line == 1
    assert data.diagnostics == [{"line": 4, "code": "record"}]


@pytest.mark.parametrize(
    "settings", [Settings(max_bytes=10), Settings(max_line_bytes=10), Settings(max_events=1)]
)
def test_resource_limits_stop_instead_of_returning_clean_report(tmp_path, settings):
    with pytest.raises(AuthLensError, match="limit"):
        ingest(write_events(tmp_path / "events", 2), settings)


def test_exclusions_and_duplicate_override(tmp_path):
    path = write_events(tmp_path / "events")
    path.write_bytes(path.read_bytes() + b"\n" + path.read_bytes())
    assert len(ingest(path, Settings(keep_duplicates=True)).events) == 2
    data = ingest(path, Settings(exclude_cidr=("192.0.2.0/24",)))
    assert not data.events and data.summary["excluded"] == 2


def test_strict_and_utf8_diagnostics_do_not_echo_content(tmp_path):
    path = tmp_path / "input"
    path.write_bytes(b"\xffSECRET\n")
    data = ingest(path, Settings())
    assert data.diagnostics == [{"line": 1, "code": "encoding"}]
    with pytest.raises(AuthLensError, match="encoding"):
        ingest(path, Settings(strict=True))


def test_directory_is_rejected(tmp_path):
    with pytest.raises(AuthLensError, match="io"):
        ingest(tmp_path, Settings())


def test_legacy_rollover_not_silently_sorted(tmp_path):
    path = tmp_path / "legacy"
    path.write_text(
        "Dec 31 23:59:59 h sshd[1]: Failed password for a from 192.0.2.1 port 22\n"
        "Jan  1 00:00:01 h sshd[1]: Accepted password for a from 192.0.2.1 port 22\n"
    )
    with pytest.raises(AuthLensError, match="legacy_order"):
        ingest(path, Settings(input_format="ssh", year=2026, timezone="+00:00"))
