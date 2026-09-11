"""Deterministic inclusive sliding windows; one representative per rule/group."""

import hashlib
import json
from collections import Counter, defaultdict, deque
from datetime import timedelta
from itertools import islice

from authlens.config import Settings
from authlens.models import Event, Finding


def _finding(
    rule: str,
    window: deque,
    current: Event,
    count: int,
    accounts: int,
    username: str | None,
    success: bool = False,
) -> Finding:
    # Preserve the most recent event (including a success) in the bounded evidence sample.
    total = count + int(success)
    evidence = tuple(islice(window, 19)) if total > 20 else tuple(window)
    if success or total > 20:
        evidence += (current,)
    identity = [
        rule,
        "1",
        current.host,
        current.service,
        current.source_ip,
        username,
        window[0].event_id,
        current.event_id,
    ]
    digest = hashlib.sha256(json.dumps(identity, ensure_ascii=True).encode()).hexdigest()[:24]
    return Finding(
        digest,
        rule,
        "HIGH" if success else "MEDIUM",
        "low" if rule == "AL-002" else "medium",
        window[0].timestamp,
        current.timestamp,
        current.host,
        current.service,
        current.source_ip,
        username,
        total,
        accounts,
        evidence,
        total > len(evidence),
    )


def detect(events: list[Event], settings: Settings) -> list[Finding]:
    """Pure correlation over canonical events; caller owns parsing and exclusions."""
    sources = defaultdict(deque)
    accounts = defaultdict(deque)
    breadth = defaultdict(Counter)
    emitted = set()
    findings = []
    delta = timedelta(seconds=settings.window_seconds)
    for event in sorted(events, key=lambda item: (item.timestamp, item.line)):
        source = (event.host, event.service, event.source_ip)
        account = (*source, event.username)
        source_window, user_window = sources[source], accounts[account]
        counts = breadth[source]
        # Compare elapsed time instead of subtracting from datetime.min.
        while source_window and event.timestamp - source_window[0].timestamp > delta:
            old = source_window.popleft()
            counts[old.username] -= 1
            if counts[old.username] == 0:
                del counts[old.username]
        while user_window and event.timestamp - user_window[0].timestamp > delta:
            user_window.popleft()
        if event.outcome == "failure":
            source_window.append(event)
            user_window.append(event)
            counts[event.username] += 1
            for rule, key, window, matched, distinct, username in (
                (
                    "AL-001",
                    account,
                    user_window,
                    len(user_window) >= settings.burst_threshold,
                    1,
                    event.username,
                ),
                (
                    "AL-002",
                    source,
                    source_window,
                    len(counts) >= settings.spray_threshold,
                    len(counts),
                    None,
                ),
            ):
                if matched and (rule, key) not in emitted:
                    findings.append(_finding(rule, window, event, len(window), distinct, username))
                    emitted.add((rule, key))
        elif len(user_window) >= settings.success_threshold and ("AL-003", account) not in emitted:
            findings.append(
                _finding(
                    "AL-003", user_window, event, len(user_window), 1, event.username, success=True
                )
            )
            emitted.add(("AL-003", account))
    return sorted(findings, key=lambda f: (f.end, f.rule_id, f.finding_id))
