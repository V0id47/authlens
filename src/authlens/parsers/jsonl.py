"""Strict normalized JSONL; rejects duplicate fields and implicit timestamps."""

import json

from authlens.config import Settings
from authlens.errors import AuthLensError
from authlens.models import Event
from authlens.parsers.common import event_from_fields


def _unique_object(pairs: list[tuple]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise AuthLensError("record")
        result[key] = value
    return result


def parse_jsonl(line: str, number: int, settings: Settings) -> Event | None:
    if not line.strip():
        return None
    try:
        data = json.loads(line, object_pairs_hook=_unique_object)
    except (ValueError, RecursionError):
        raise AuthLensError("record") from None
    if not isinstance(data, dict):
        raise AuthLensError("record")
    return event_from_fields(data, number)
