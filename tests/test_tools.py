"""Tests for duet.tools."""

import json

from duet.tools import DECLINED, TOOLS, run_tool
from helpers import always


def test_the_two_tools_are_defined():
    assert [tool["name"] for tool in TOOLS] == ["read_inbox", "send_message"]


def test_every_tool_is_strict_with_a_closed_schema():
    for tool in TOOLS:
        assert tool["strict"] is True
        assert tool["input_schema"]["type"] == "object"
        assert tool["input_schema"]["additionalProperties"] is False


def test_send_message_requires_to_and_text():
    schema = TOOLS[1]["input_schema"]
    assert schema["required"] == ["to", "text"]
    assert set(schema["properties"]) == {"to", "text"}


def test_read_inbox_returns_the_inbox_as_json(inbox):
    result = run_tool("read_inbox", {}, inbox, always(True))
    assert json.loads(result) == inbox


def test_an_approved_message_is_sent_and_reported(inbox):
    sent, printed = [], []
    result = run_tool(
        "send_message",
        {"to": "Sara", "text": "Hi"},
        inbox,
        always(True),
        send=lambda to, text: sent.append((to, text)),
        out=printed.append,
    )
    assert result == "Sent."
    assert sent == [("Sara", "Hi")]
    assert printed == ["Sent."]


