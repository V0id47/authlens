"""Local file boundaries. Destination directories must be operator-controlled."""

import os
import stat
from contextlib import contextmanager
from pathlib import Path

from authlens.errors import AuthLensError


@contextmanager
def open_input(path: Path):
    descriptor = None
    try:
        before = path.lstat()
        if not stat.S_ISREG(before.st_mode):
            raise AuthLensError("io", 3)
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        descriptor = os.open(path, flags)
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or not os.path.samestat(before, opened):
            raise AuthLensError("io", 3)
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = None  # ownership transferred
            yield stream, opened
    except OSError:
        raise AuthLensError("io", 3) from None
    finally:
        if descriptor is not None:
            os.close(descriptor)


@contextmanager
def new_output(path: Path, *, keep_on_error: bool = False):
    """Exclusive creation. Never unlink a pre-existing destination on failure."""
    created = False
    try:
        descriptor = os.open(
            path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0), 0o600
        )
        created = True
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
            yield stream
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException as error:
        if created and not keep_on_error:
            try:
                path.unlink()
            except OSError:
                pass
        if isinstance(error, OSError):
            raise AuthLensError("output", 3) from None
        raise
