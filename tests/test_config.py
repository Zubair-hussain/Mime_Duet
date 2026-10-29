"""Tests for duet.config."""

import json

import pytest

from duet.config import DEFAULT_SYSTEM, MODEL, Settings, load_settings, validate


def test_defaults_match_the_video():
    settings = Settings()
    assert settings.model == "claude-opus-5-5"
    assert settings.effort == "medium"
    assert settings.max_tokens == 16000
    assert settings.check_every_seconds == 10800
    assert settings.system == DEFAULT_SYSTEM


def test_missing_default_file_gives_defaults(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert load_settings() == Settings()


def test_missing_explicit_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_settings(tmp_path / "nope.json")


def test_file_overrides_defaults(tmp_path):
    file = tmp_path / "config.json"
    file.write_text(json.dumps({"effort": "high", "check_every_seconds": 60}))
    settings = load_settings(file)
    assert settings.effort == "high"
    assert settings.check_every_seconds == 60
    assert settings.model == MODEL


def test_invalid_json_raises(tmp_path):
    file = tmp_path / "config.json"
    file.write_text("{not json")
    with pytest.raises(ValueError, match="not valid JSON"):
        load_settings(file)


def test_non_object_json_raises(tmp_path):
    file = tmp_path / "config.json"
    file.write_text("[1, 2]")
    with pytest.raises(ValueError, match="JSON object"):
        load_settings(file)


def test_unknown_setting_raises(tmp_path):
    file = tmp_path / "config.json"
    file.write_text(json.dumps({"colour": "blue"}))
    with pytest.raises(ValueError, match="Unknown setting"):
        load_settings(file)


@pytest.mark.parametrize(
    "name,value",
    [
        ("check_every_seconds", 0),
        ("check_every_seconds", -5),
        ("max_tokens", 0),
        ("check_every_seconds", "soon"),
        ("check_every_seconds", True),
    ],
)
def test_bad_numbers_are_rejected(name, value):
    with pytest.raises(ValueError, match="positive whole number"):
        validate(Settings(**{name: value}))


def test_bad_effort_is_rejected():
    with pytest.raises(ValueError, match="effort must be one of"):
        validate(Settings(effort="extreme"))


@pytest.mark.parametrize("name", ["model", "effort", "inbox_path", "system"])
def test_empty_text_settings_are_rejected(name):
    with pytest.raises(ValueError, match="non-empty string"):
        validate(Settings(**{name: "  "}))


def test_valid_settings_pass_through_unchanged():
    settings = Settings()
    assert validate(settings) is settings


def test_the_bundled_config_file_is_valid():
    from pathlib import Path

    bundled = Path(__file__).resolve().parent.parent / "duet.config.json"
    assert load_settings(bundled) == Settings()
