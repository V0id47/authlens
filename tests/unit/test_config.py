import pytest

from authlens.config import Settings, read_config
from authlens.errors import AuthLensError


@pytest.mark.parametrize(
    "config",
    [
        {"burst_threshold": True},
        {"window_seconds": 0},
        {"max_events": 500001},
        {"language": "fr"},
        {"exclude_cidr": ["not-ip"]},
        {"exclude_user": "alice"},
        {"unknown": 1},
        {"timezone": "+25:00"},
        {"strict": "false"},
    ],
)
def test_invalid_config_rejected(config):
    with pytest.raises(AuthLensError):
        Settings.from_mapping(config)


def test_toml_and_cli_override(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text('language = "es"\nwindow_seconds = 120\n', encoding="utf-8")
    settings = Settings.from_mapping(read_config(path) | {"window_seconds": 60})
    assert (settings.language, settings.window_seconds) == ("es", 60)


def test_bad_toml_never_exposes_values(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text('language = "SECRET', encoding="utf-8")
    with pytest.raises(AuthLensError) as error:
        read_config(path)
    assert "SECRET" not in str(error.value)
