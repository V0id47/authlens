"""Canonical validation shared by the supported grammars."""

import ipaddress
import re
from datetime import UTC, datetime

from authlens.config import valid_identity
from authlens.errors import AuthLensError
from authlens.models import Event


def timestamp(value: str) -> datetime:
    if not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})", value
    ):
        raise AuthLensError("record")
    # datetime accepts overflowing offset minutes; our interchange contract does not.
    if not value.endswith("Z") and (int(value[-5:-3]) > 23 or int(value[-2:]) > 59):
        raise AuthLensError("record")
    try:
        return datetime.fromisoformat(value).astimezone(UTC)
    except (ValueError, OverflowError):
        raise AuthLensError("record") from None


def event_from_fields(data: dict, line: int) -> Event:
    expected = {"timestamp", "host", "service", "username", "source_ip", "outcome"}
    if set(data) != expected or not all(valid_identity(v) for v in data.values()):
        raise AuthLensError("record")
    if data["outcome"] not in ("failure", "success") or "%" in data["source_ip"]:
        raise AuthLensError("record")
    try:
        address = ipaddress.ip_address(data["source_ip"])
    except ValueError:
        raise AuthLensError("record") from None
    if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped:
        address = address.ipv4_mapped
    return Event(
        timestamp=timestamp(data["timestamp"]),
        host=data["host"],
        service=data["service"],
        username=data["username"],
        source_ip=str(address),
        outcome=data["outcome"],
        line=line,
    )
