"""Bounded ingestion with source hashing and explicit data-quality accounting."""

import hashlib
import ipaddress
import os
from dataclasses import replace
from pathlib import Path

from authlens.config import Settings
from authlens.errors import AuthLensError
from authlens.models import Dataset
from authlens.parsers.jsonl import parse_jsonl
from authlens.parsers.ssh import is_legacy, parse_ssh
from authlens.safeio import open_input


def ingest(path: Path, settings: Settings) -> Dataset:
    parser = parse_jsonl if settings.input_format == "jsonl" else parse_ssh
    summary = dict(
        sha256="",
        bytes=0,
        lines=0,
        accepted=0,
        ignored=0,
        malformed=0,
        excluded=0,
        duplicates=0,
        analyzed=0,
        complete=True,
    )
    diagnostics = []
    events = []
    seen = set()
    networks = [ipaddress.ip_network(value) for value in settings.exclude_cidr]
    users = set(settings.exclude_user)
    previous_legacy = None
    hasher = hashlib.sha256()
    with open_input(path) as (stream, before):
        if before.st_size > settings.max_bytes:
            raise AuthLensError("limit", 3)
        while raw := stream.readline(min(settings.max_line_bytes, settings.max_bytes) + 1):
            summary["bytes"] += len(raw)
            summary["lines"] += 1
            number = summary["lines"]
            if len(raw) > settings.max_line_bytes or summary["bytes"] > settings.max_bytes:
                raise AuthLensError("limit", 3)
            hasher.update(raw)
            try:
                try:
                    text = raw.decode("utf-8")
                except UnicodeError:
                    raise AuthLensError("encoding") from None
                # A UTF-8 BOM is permitted only at the very beginning.
                if number == 1:
                    text = text.removeprefix("\ufeff")
                event = parser(text, number, settings)
            except AuthLensError as error:
                if settings.strict:
                    raise AuthLensError(error.code, 4) from None
                summary["malformed"] += 1
                summary["complete"] = False
                if len(diagnostics) < 20:
                    diagnostics.append({"line": number, "code": error.code})
                continue
            if event is None:
                summary["ignored"] += 1
                continue
            summary["accepted"] += 1
            if summary["accepted"] > settings.max_events:
                raise AuthLensError("limit", 3)
            if settings.input_format == "ssh" and is_legacy(text):
                if previous_legacy is not None and event.timestamp < previous_legacy:
                    raise AuthLensError("legacy_order", 4)
                previous_legacy = event.timestamp
            address = ipaddress.ip_address(event.source_ip)
            if event.username in users or any(address in network for network in networks):
                summary["excluded"] += 1
                continue
            key = event.identity()
            if not settings.keep_duplicates and key in seen:
                summary["duplicates"] += 1
                continue
            seen.add(key)
            events.append(event)
        after = os.fstat(stream.fileno())
        if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
        ) or summary["bytes"] != after.st_size:
            raise AuthLensError("input_changed", 3)
    digest = hasher.hexdigest()
    summary["sha256"] = digest
    summary["analyzed"] = len(events)
    summary["complete"] = summary["complete"] and bool(events)
    events = [replace(event, event_id=f"{digest}:{event.line}") for event in events]
    events.sort(key=lambda event: (event.timestamp, event.line))
    return Dataset(events, summary, diagnostics)
