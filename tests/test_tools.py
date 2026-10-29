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


def test_an_approved_message_works_without_a_send_hook(inbox):
    result = run_tool(
        "send_message", {"to": "Sara", "text": "Hi"}, inbox, always(True), out=lambda text: None
    )
    assert result == "Sent."


def test_a_declined_message_is_not_sent(inbox):
    sent = []
    result = run_tool(
        "send_message",
        {"to": "Sara", "text": "Hi"},
        inbox,
        always(False),
        send=lambda to, text: sent.append((to, text)),
    )
    assert result == DECLINED
    assert sent == []


def test_approval_receives_the_recipient_and_the_text(inbox):
    seen = []
    run_tool(
        "send_message",
        {"to": "Sara", "text": "Hi"},
        inbox,
        lambda to, text: seen.append((to, text)) or True,
        out=lambda text: None,
    )
    assert seen == [("Sara", "Hi")]


def test_an_unknown_tool_is_reported(inbox):
    assert (
        run_tool("delete_everything", {}, inbox, always(True)) == "Unknown tool: delete_everything"
    )
