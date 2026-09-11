"""Bounded OpenSSH auth-line grammar, not a generic syslog parser."""

import re
from datetime import datetime

from authlens.config import Settings
from authlens.errors import AuthLensError
from authlens.models import Event
from authlens.parsers.common import event_from_fields

_AUTH = re.compile(
    r"^(?P<prefix>.+?) (?P<host>\S+) sshd(?:-session)?(?:\[\d+\])?: "
    r"(?P<action>Failed|Accepted) (?:password|publickey|keyboard-interactive/pam) "
    r"for (?:invalid user )?(?P<user>\S+) from (?P<ip>\S+) port (?P<port>\d+)"
    r"(?:\s.*)?$"
)
_LEGACY = re.compile(
    r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) +"
    r"(\d{1,2}) (\d{2}):(\d{2}):(\d{2})$"
)
_MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def is_legacy(line: str) -> bool:
    return bool(re.match(r"^[A-Z][a-z]{2} +\d{1,2} \d{2}:\d{2}:\d{2} ", line))


def parse_ssh(line: str, number: int, settings: Settings) -> Event | None:
    match = _AUTH.fullmatch(line.rstrip("\r\n"))
    if not match:
        if "sshd" in line and ("Failed " in line or "Accepted " in line):
            raise AuthLensError("record")
        return None
    fields = match.groupdict()
    if (
        len(fields["port"]) > 5
        or not fields["port"].isascii()
        or not 1 <= int(fields["port"]) <= 65535
    ):
        raise AuthLensError("record")
    stamp = fields["prefix"]
    legacy = _LEGACY.fullmatch(stamp)
    if legacy:
        if settings.year is None or settings.timezone is None:
            raise AuthLensError("legacy_time")
        month, day, hour, minute, second = legacy.groups()
        try:
            stamp = (
                datetime(
                    settings.year,
                    _MONTHS.index(month) + 1,
                    int(day),
                    int(hour),
                    int(minute),
                    int(second),
                ).isoformat()
                + settings.timezone
            )
        except ValueError:
            raise AuthLensError("record") from None
    return event_from_fields(
        {
            "timestamp": stamp,
            "host": fields["host"],
            "service": "ssh",
            "username": fields["user"],
            "source_ip": fields["ip"],
            "outcome": "failure" if fields["action"] == "Failed" else "success",
        },
        number,
    )
