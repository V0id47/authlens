import json
from datetime import UTC, datetime

import pytest

from authlens.config import Settings
from authlens.errors import AuthLensError
from authlens.parsers.jsonl import parse_jsonl
from authlens.parsers.ssh import parse_ssh


def record(**changes):
    data = dict(
        timestamp="2026-01-01T01:00:00+01:00",
        host="lab",
        service="ssh",
        username="用户",
        source_ip="::ffff:192.0.2.4",
        outcome="failure",
    )
    return json.dumps(data | changes)


def test_json_normalizes_time_ip_and_preserves_unicode():
    event = parse_jsonl(record(), 7, Settings())
    assert event.timestamp == datetime(2026, 1, 1, tzinfo=UTC)
    assert event.username == "用户"
    assert event.source_ip == "192.0.2.4"
    assert event.line == 7


@pytest.mark.parametrize(
    "changes",
    [
        {"timestamp": "2026-01-01T00:00:00"},
        {"timestamp": "2026-01-01"},
        {"source_ip": "example.com"},
        {"source_ip": "fe80::1%eth0"},
        {"outcome": True},
        {"outcome": "unknown"},
        {"username": "bad\x1b[31m"},
        {"host": ""},
        {"username": "x" * 257},
        {"token": "DO_NOT_ECHO"},
        {"service": None},
    ],
)
def test_json_rejects_ambiguous_or_unsafe_records(changes):
    with pytest.raises(AuthLensError):
        parse_jsonl(record(**changes), 1, Settings())


@pytest.mark.parametrize("line", ["[]", '{"host":"a","host":"b"}', "{", "null"])
def test_json_rejects_invalid_shape_and_duplicate_fields(line):
    with pytest.raises(AuthLensError):
        parse_jsonl(line, 1, Settings())


def test_ssh_ignores_raw_suffix_and_handles_invalid_user():
    line = (
        "2026-01-01T00:00:00Z host sshd[123]: Failed password for invalid user "
        "alice from 2001:db8::1 port 1234 ssh2 SENSITIVE_SUFFIX"
    )
    event = parse_ssh(line, 2, Settings())
    assert (event.username, event.source_ip, event.outcome) == ("alice", "2001:db8::1", "failure")
    assert "SENSITIVE_SUFFIX" not in repr(event)


def test_ssh_session_accepted_key():
    event = parse_ssh(
        "2026-01-01T00:00:00Z host sshd-session[4]: Accepted publickey for "
        "root from 192.0.2.1 port 22 ssh2",
        1,
        Settings(),
    )
    assert event.outcome == "success"


def test_legacy_requires_explicit_year_and_offset():
    line = "Jan  1 00:00:00 host sshd[1]: Failed password for a from 192.0.2.1 port 22"
    with pytest.raises(AuthLensError, match="legacy_time"):
        parse_ssh(line, 1, Settings())
    event = parse_ssh(line, 1, Settings(year=2026, timezone="-03:00"))
    assert event.timestamp == datetime(2026, 1, 1, 3, tzinfo=UTC)


def test_unrelated_line_ignored_but_broken_auth_is_malformed():
    assert parse_ssh("Jan 1 host cron[3]: hello", 1, Settings()) is None
    with pytest.raises(AuthLensError):
        parse_ssh("host sshd[1]: Failed password for a from invalid port 99999", 1, Settings())
