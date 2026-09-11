import random
from datetime import UTC, datetime, timedelta

from authlens.config import Settings
from authlens.engine import detect
from authlens.models import Event

BASE = datetime(2026, 1, 1, tzinfo=UTC)


def event(t, user="a", outcome="failure", host="h", service="ssh", ip="192.0.2.1", line=None):
    number = t + 1 if line is None else line
    return Event(BASE + timedelta(seconds=t), host, service, user, ip, outcome, number, str(number))


def test_burst_inclusive_boundary_and_success_correlation():
    events = [event(i) for i in [0, 1, 2, 3, 300]] + [event(300, outcome="success", line=400)]
    findings = detect(events, Settings())
    assert [f.rule_id for f in findings] == ["AL-001", "AL-003"]
    assert [f.event_count for f in findings] == [5, 6]
    assert findings[1].severity == "HIGH"


def test_window_expiry_and_success_before_failures():
    events = [event(0, outcome="success")] + [event(i) for i in [1, 2, 3, 4, 302]]
    assert detect(events, Settings()) == []


def test_breadth_counts_distinct_users_and_never_crosses_host_service():
    assert [f.rule_id for f in detect([event(i, user=str(i)) for i in range(5)], Settings())] == [
        "AL-002"
    ]
    events = [event(i, host=str(i), service=str(i)) for i in range(10)]
    assert detect(events, Settings()) == []


def test_success_requires_same_account_and_source():
    events = [event(i) for i in range(5)]
    events += [event(6, user="b", outcome="success"), event(7, ip="192.0.2.2", outcome="success")]
    assert [f.rule_id for f in detect(events, Settings())] == ["AL-001"]


def test_only_first_episode_and_bounded_evidence():
    events = [event(i) for i in range(50)]
    findings = detect(events, Settings(burst_threshold=30))
    assert len(findings) == 1
    assert findings[0].event_count == 30 and len(findings[0].evidence) == 20
    assert findings[0].evidence_truncated


def test_randomized_against_independent_bruteforce_oracle():
    rng = random.Random(420)
    settings = Settings(
        window_seconds=10, burst_threshold=3, spray_threshold=3, success_threshold=3
    )
    for _ in range(50):
        events = [
            event(
                rng.randrange(50),
                user=str(rng.randrange(4)),
                host=str(rng.randrange(2)),
                outcome=rng.choice(["failure", "failure", "success"]),
                line=i,
            )
            for i in range(80)
        ]
        ordered = sorted(events, key=lambda e: (e.timestamp, e.line))
        expected = set()
        for i, current in enumerate(ordered):
            group = (current.host, current.service, current.source_ip)
            recent = [
                e
                for e in ordered[: i + 1]
                if e.outcome == "failure"
                and (e.host, e.service, e.source_ip) == group
                and 0 <= (current.timestamp - e.timestamp).total_seconds() <= 10
            ]
            same = [e for e in recent if e.username == current.username]
            if current.outcome == "failure" and len(same) >= 3:
                expected.add(("AL-001", *group, current.username))
            if current.outcome == "failure" and len({e.username for e in recent}) >= 3:
                expected.add(("AL-002", *group, None))
            if current.outcome == "success" and len(same) >= 3:
                expected.add(("AL-003", *group, current.username))
        actual = {
            (f.rule_id, f.host, f.service, f.source_ip, f.username)
            for f in detect(events, settings)
        }
        assert actual == expected
