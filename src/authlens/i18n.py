"""Packaged message catalogs with explicit language precedence."""

import json
import locale
import os
from importlib.resources import files

from authlens.errors import AuthLensError

LANGUAGES = ("en", "es", "ru", "zh-CN")


def choose_language(explicit: str | None) -> str:
    if explicit is not None:
        if explicit not in LANGUAGES:
            raise AuthLensError("language")
        return explicit
    detected = next(
        (os.environ[key] for key in ("LC_ALL", "LC_MESSAGES", "LANG") if os.environ.get(key)), None
    )
    if not detected:
        try:
            detected = locale.getlocale()[0]
        except (ValueError, TypeError):
            detected = None
    prefix = (detected or "en").lower().replace("_", "-").split("-")[0].split(".")[0]
    return "zh-CN" if prefix == "zh" else prefix if prefix in LANGUAGES else "en"


class Translator:
    def __init__(self, language: str):
        if language not in LANGUAGES:
            raise AuthLensError("language")
        self.language = language
        root = files("authlens").joinpath("locales")
        self.messages = json.loads(root.joinpath(f"{language}.json").read_text(encoding="utf-8"))

    def __call__(self, key: str, **parameters) -> str:
        return self.messages[key].format(**parameters)
