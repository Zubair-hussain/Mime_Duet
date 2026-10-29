"""Tests for mini_duet.py, the single-file version shown in the video."""

import json
from types import SimpleNamespace

import pytest

import mini_duet
from helpers import FakeClient, response, text_block, tool_use_block


def test_settings_match_the_video():
    assert mini_duet.MODEL == "claude-opus-5-5"
    assert mini_duet.CHECK_EVERY_SECONDS == 3 * 60 * 60


def test_two_tools_are_defined():
    assert [tool["name"] for tool in mini_duet.tools] == ["read_inbox", "send_message"]


def test_read_inbox_returns_the_demo_inbox():
    assert json.loads(mini_duet.run_tool("read_inbox", {})) == mini_duet.INBOX


def test_a_message_is_sent_only_after_approval(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt: "y")
    assert mini_duet.run_tool("send_message", {"to": "Sara", "text": "Hi"}) == "Sent."
    assert "Sara" in capsys.readouterr().out


def test_a_declined_message_is_not_sent(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "n")
    result = mini_duet.run_tool("send_message", {"to": "Sara", "text": "Hi"})
    assert result == "The user declined. Do not send this message."


def test_an_unknown_tool_is_reported():
    assert mini_duet.run_tool("nope", {}) == "Unknown tool: nope"


@pytest.mark.parametrize(
    "answer,expected", [("y", True), ("Y", True), (" y ", True), ("n", False), ("", False)]
)
def test_ask_approval_only_accepts_y(monkeypatch, answer, expected):
    monkeypatch.setattr("builtins.input", lambda prompt: answer)
    assert mini_duet.ask_approval("Sara", "Hi") is expected


def test_check_in_runs_the_tool_loop_and_prints_the_brief(monkeypatch, capsys):
    fake = FakeClient(
        response("tool_use", tool_use_block("t1", "read_inbox")),
        response("end_turn", text_block("Two things need you.")),
    )
    monkeypatch.setattr(mini_duet, "client", fake)
    mini_duet.check_in()
    assert fake.calls[0]["model"] == "claude-opus-5-5"
    assert fake.calls[0]["fallbacks"] == "default"
    assert fake.calls[1]["messages"][-1]["content"][0]["tool_use_id"] == "t1"
    output = capsys.readouterr().out
    assert "--- Your brief ---" in output
    assert "Two things need you." in output


def test_check_in_skips_blocks_that_are_neither_tool_calls_nor_text(monkeypatch, capsys):
    other = SimpleNamespace(type="thinking")
    fake = FakeClient(
        response("tool_use", other, text_block("let me look"), tool_use_block("t1", "read_inbox")),
        response("end_turn", other, text_block("All done.")),
    )
    monkeypatch.setattr(mini_duet, "client", fake)
    mini_duet.check_in()
    results = fake.calls[1]["messages"][-1]["content"]
    assert [result["tool_use_id"] for result in results] == ["t1"]
    assert "All done." in capsys.readouterr().out


