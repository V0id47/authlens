"""Closed configuration schema; command-line overrides use the same validator."""

import ipaddress
import re
import tomllib
import unicodedata
from dataclasses import dataclass, fields
from pathlib import Path

from authlens.errors import AuthLensError


def valid_offset(value: str) -> bool:
    return bool(re.fullmatch(r"[+-](?:0\d|1\d|2[0-3]):[0-5]\d", value))


def valid_identity(value: object) -> bool:
    return (
        isinstance(value, str)
        and 0 < len(value) <= 256
        and not any(unicodedata.category(c).startswith("C") for c in value)
        and value.strip() == value
        and bool(value.strip())
    )


@dataclass(frozen=True, slots=True)
class Settings:
    language: str | None = None
    input_format: str = "jsonl"
    window_seconds: int = 300
    burst_threshold: int = 5
    spray_threshold: int = 5
    success_threshold: int = 5
    max_bytes: int = 16 * 1024 * 1024
    max_line_bytes: int = 16 * 1024
    max_events: int = 50_000
    year: int | None = None
    timezone: str | None = None
    exclude_cidr: tuple[str, ...] = ()
    exclude_user: tuple[str, ...] = ()
    keep_duplicates: bool = False
    strict: bool = False

    @classmethod
    def from_mapping(cls, values: dict) -> "Settings":
        if not isinstance(values, dict) or set(values) - {f.name for f in fields(cls)}:
            raise AuthLensError("config")
        ranges = {
            "window_seconds": (1, 86400),
            "burst_threshold": (2, 10000),
            "spray_threshold": (2, 10000),
            "success_threshold": (2, 10000),
            "max_bytes": (1, 256 * 1024 * 1024),
            "max_line_bytes": (1, 1024 * 1024),
            "max_events": (1, 500000),
            "year": (1, 9999),
        }
        data = dict(values)
        for key, value in data.items():
            if key in ranges:
                low, high = ranges[key]
                if type(value) is not int or not low <= value <= high:
                    raise AuthLensError("config")
            elif key in ("keep_duplicates", "strict"):
                if type(value) is not bool:
                    raise AuthLensError("config")
            elif key in ("exclude_cidr", "exclude_user"):
                if not isinstance(value, (list, tuple)) or len(value) > 256:
                    raise AuthLensError("config")
                if not all(valid_identity(item) for item in value):
                    raise AuthLensError("config")
                if key == "exclude_cidr":
                    try:
                        for item in value:
                            ipaddress.ip_network(item, strict=True)
                    except ValueError:
                        raise AuthLensError("config") from None
                data[key] = tuple(value)
            elif key == "language" and value not in ("es", "en", "ru", "zh-CN"):
                raise AuthLensError("language")
            elif key == "input_format" and value not in ("ssh", "jsonl"):
                raise AuthLensError("config")
            elif key == "timezone" and (not isinstance(value, str) or not valid_offset(value)):
                raise AuthLensError("config")
        return cls(**data)


def read_config(path: Path) -> dict:
    try:
        if path.is_symlink() or not path.is_file():
            raise AuthLensError("io", 3)
        with path.open("rb") as stream:
            raw = stream.read(65537)
        if len(raw) > 65536:
            raise AuthLensError("config")
        data = tomllib.loads(raw.decode("utf-8"))
        Settings.from_mapping(data)
        return data
    except (ValueError, UnicodeError, RecursionError):
        raise AuthLensError("config") from None
    except OSError:
        raise AuthLensError("io", 3) from None
