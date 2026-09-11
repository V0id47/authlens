from datetime import UTC, datetime, timedelta

import pytest

from authlens.config import Settings
from authlens.engine import detect
from authlens.errors import AuthLensError
from authlens.models import Event

BASE = datetime(2026, 1, 1, tzinfo=UTC)


def event(
    offset,
    *,
    username="alice",
    source="192.0.2.50",
    host="h",
    service="ssh",
    outcome="failure",
    line=1,
):
    return Event(
        BASE + timedelta(seconds=offset),
        host,
        service,
        username,
        source,
        outcome,
        line,
        f"event-{line}",
    )


def test_one_microsecond_outside_window_does_not_trigger():
    events = [
        event(0, line=1),
        event(1, line=2),
        event(2, line=3),
        event(3, line=4),
        event(300.000001, line=5),
    ]
    assert detect(events, Settings()) == []


def test_equal_timestamp_success_sees_only_prior_lines():
    failures = [event(0, line=i) for i in range(1, 6)]
    success_first = event(0, outcome="success", line=0)
    success_last = event(0, outcome="success", line=10)
    assert [finding.rule_id for finding in detect([success_first, *failures], Settings())] == [
        "AL-001"
    ]
    assert [finding.rule_id for finding in detect([*failures, success_last], Settings())] == [
        "AL-001",
        "AL-003",
    ]


def test_adversarial_group_boundaries_do_not_cross_fields():
    events = [
        event(
            i,
            host=f"host-{i}",
            service=f"svc-{i}",
            source=f"192.0.2.{i + 60}",
            username=f"user-{i}",
            line=i,
        )
        for i in range(5)
    ]
    assert detect(events, Settings()) == []


@pytest.mark.parametrize(
    "mapping",
    [
        {"burst_threshold": 1},
        {"spray_threshold": 1},
        {"success_threshold": 1},
        {"max_bytes": 0},
        {"max_line_bytes": 0},
        {"max_events": 0},
    ],
)
def test_threshold_and_resource_lower_bounds_cannot_disable_safeguards(mapping):
    with pytest.raises(AuthLensError):
        Settings.from_mapping(mapping)
