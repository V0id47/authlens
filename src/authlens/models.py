"""Boundary contracts shared by ingestion, detection and presentation."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Event:
    timestamp: datetime
    host: str
    service: str
    username: str
    source_ip: str
    outcome: str
    line: int
    event_id: str = ""

    def identity(self) -> tuple:
        return (
            self.timestamp,
            self.host,
            self.service,
            self.username,
            self.source_ip,
            self.outcome,
        )


@dataclass(slots=True)
class Dataset:
    events: list[Event]
    summary: dict
    diagnostics: list[dict] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class Finding:
    finding_id: str
    rule_id: str
    severity: str
    confidence: str
    start: datetime
    end: datetime
    host: str
    service: str
    source_ip: str
    username: str | None
    event_count: int
    account_count: int
    evidence: tuple[Event, ...]
    evidence_truncated: bool


SEVERITIES = ("INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL")
