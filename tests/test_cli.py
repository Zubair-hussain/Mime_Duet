"""Tests for duet.cli."""

import json
import runpy
import sys

import anthropic
import pytest

from duet import __version__
from duet.cli import AUTH_HELP, main
from helpers import FakeClient, response, text_block, tool_use_block


def quiet_client():
    return FakeClient(response("end_turn", text_block("All quiet.")))


def write_json(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


class RaisingClient:
    """A client whose requests fail with whatever error we give it."""

    def __init__(self, error):
        self.beta = type(
            "Beta", (), {"messages": type("Messages", (), {"create": self._create})()}
        )()
        self._error = error

    def _create(self, **kwargs):
        raise self._error


class FakeAuthError(anthropic.AuthenticationError):
    """An authentication error we can build without a real HTTP response."""

    def __init__(self):
        Exception.__init__(self, "invalid x-api-key")


def test_once_runs_a_single_check_in(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    client = quiet_client()
    assert main(["--once"], client_factory=lambda: client) == 0
    assert len(client.calls) == 1
    assert "All quiet." in capsys.readouterr().out


def test_config_and_inbox_files_are_used(tmp_path):
    config = write_json(tmp_path / "config.json", {"effort": "high", "max_tokens": 99})
    inbox = write_json(tmp_path / "inbox.json", [{"from": "A", "subject": "B", "body": "C"}])
    client = quiet_client()
    main(["--once", "--config", str(config), "--inbox", str(inbox)], client_factory=lambda: client)
    assert client.calls[0]["output_config"] == {"effort": "high"}
    assert client.calls[0]["max_tokens"] == 99


def test_the_inbox_path_comes_from_the_config_by_default(tmp_path):
    inbox = write_json(tmp_path / "mine.json", [{"from": "Sentinel", "subject": "S", "body": "S"}])
    config = write_json(tmp_path / "config.json", {"inbox_path": str(inbox)})
    client = FakeClient(
        response("tool_use", tool_use_block("t1", "read_inbox")),
        response("end_turn", text_block("Done.")),
    )
    main(["--once", "--config", str(config)], client_factory=lambda: client)
    assert "Sentinel" in client.calls[1]["messages"][-1]["content"][0]["content"]


def test_a_broken_config_exits_with_code_2(tmp_path, capsys):
    config = tmp_path / "bad.json"
    config.write_text("{nope")
    assert main(["--once", "--config", str(config)], client_factory=quiet_client) == 2
    assert "Config error" in capsys.readouterr().out


def test_a_missing_config_file_exits_with_code_2(tmp_path, capsys):
    assert (
        main(["--once", "--config", str(tmp_path / "missing.json")], client_factory=quiet_client)
        == 2
    )
    assert "not found" in capsys.readouterr().out


